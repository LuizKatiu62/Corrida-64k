const CACHE = 'desafio64-v93';

// Core app files — cached on install
const CORE_ASSETS = [
  './index.html',
  './app.html',
  './dashboard.html',
  './convite.html',
  './convite-pt.html',
  './goodbye.html',
  './goodbye-pt.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './login-bg.jpg',
];

// External scripts — cached on first fetch, served from cache when offline
const EXT_URLS = [
  'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js',
  'https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js',
  'https://www.gstatic.com/firebasejs/9.23.0/firebase-database-compat.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(async c => {
      // Cache core assets (must succeed)
      await c.addAll(CORE_ASSETS);
      // Cache external scripts best-effort (don't fail install if offline)
      await Promise.allSettled(
        EXT_URLS.map(url =>
          fetch(url, {cache:'force-cache'})
            .then(res => { if(res.ok) c.put(url, res); })
            .catch(()=>{})
        )
      );
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => {
      // Tell all open tabs to reload so they get the new version
      return self.clients.matchAll({ includeUncontrolled: true, type: 'window' })
        .then(clients => clients.forEach(client => client.postMessage({ type: 'SW_UPDATED' })));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if(e.request.method !== 'GET') return;

  const url = e.request.url;


  // For external CDN/Firebase scripts: cache-first, no network fallback needed
  const isExt = EXT_URLS.some(u => url.startsWith(u) || url.includes('gstatic.com') || url.includes('cloudflare.com') || url.includes('unpkg.com') || url.includes('wikimedia.org'));

  if(isExt){
    e.respondWith(
      caches.match(e.request).then(cached => {
        if(cached) return cached;
        return fetch(e.request.url, {mode:'cors', credentials:'omit'}).then(res => {
          if(res.ok){
            caches.open(CACHE).then(c => c.put(e.request, res.clone()));
          }
          return res;
        }).catch(() => new Response('', {status:503}));
      })
    );
    return;
  }

  // version.json — always network, never cache (used for auto-update detection)
  if(url.includes('version.json')){
    e.respondWith(fetch(e.request, {cache:'no-store'}).catch(() => new Response('{"v":0}', {status:200})));
    return;
  }

  // For Firebase realtime database calls — network only (don't cache dynamic data)
  if(url.includes('firebaseio.com') || url.includes('firebase.googleapis.com')){
    e.respondWith(fetch(e.request).catch(() => new Response('', {status:503})));
    return;
  }

  // Weather API — always network, never cache (forecast changes daily)
  if(url.includes('open-meteo.com')){
    e.respondWith(fetch(e.request, {cache:'no-store'}).catch(() => new Response('{}', {status:200})));
    return;
  }

  // For HTML files: network-first, bypass HTTP cache to always get latest
  if(e.request.headers.get('accept')&&e.request.headers.get('accept').includes('text/html')){
    e.respondWith(
      fetch(e.request, {cache:'no-cache'}).then(res => {
        if(res.ok){
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => caches.match(e.request).then(r => r || caches.match('./convite.html')))
    );
    return;
  }

  // For everything else (app files, weather API, etc.): cache-first, fallback to convite.html
  e.respondWith(
    caches.match(e.request).then(cached => {
      if(cached) return cached;
      return fetch(e.request).then(res => {
        if(res.ok){
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => caches.match('./convite.html'));
    })
  );
});

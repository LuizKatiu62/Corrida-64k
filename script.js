// BOTÃO DE LOGIN COM STRAVA
document.getElementById("loginStrava").onclick = function () {
    const client_id = 218324;
    const redirect_uri = "https://luizkatiu62.github.io/Corrida-64k/";
    const scope = "read,activity:read,activity:read_all";

    const url =
      `https://www.strava.com/oauth/authorize?client_id=${client_id}` +
      `&response_type=code&redirect_uri=${redirect_uri}` +
      `&scope=${scope}&approval_prompt=auto`;

    window.location.href = url;
};

// CAPTURAR O TOKEN APÓS LOGIN
async function handleStravaRedirect() {
    const params = new URLSearchParams(window.location.search);

    if (params.has("code")) {
        const code = params.get("code");

        document.getElementById("status").innerText = "Autorizando…";

        const res = await fetch(
          `https://summer-surf-93af.lcdsilva46.workers.dev/exchange_token?code=${code}`
        );

        const data = await response.json();

        localStorage.setItem("strava_token", data.access_token);

        document.getElementById("status").innerText = "Conectado ao Strava!";
    }
}

handleStravaRedirect();

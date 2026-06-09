#!/usr/bin/env python3
"""
Gera PDFs dos cartões de voltas:
  cartoes-voltas.pdf   — branco com versículos
  cartoes-azul.pdf     — azul escuro com números grandes
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
import os

W, H = A4  # 595.27 x 841.89 pts

# ─── Lap data ─────────────────────────────────────────────────────────────────
laps = [
    (1,  "3,35 km",  "O meu socorro vem do Senhor,\nque fez o céu e a terra.",
     "My help comes from the Lord,\nthe Maker of heaven and earth.", "Sl / Ps 121:2"),
    (2,  "6,70 km",  "O Senhor é a minha força e o meu escudo;\nnele o meu coração confia.",
     "The Lord is my strength and my shield;\nmy heart trusts in him.", "Sl / Ps 28:7"),
    (3,  "10,05 km", "Tudo posso naquele\nque me fortalece.",
     "I can do all things through\nChrist who strengthens me.", "Fp / Ph 4:13"),
    (4,  "13,40 km", "Entrega o teu caminho ao Senhor;\nconfia nele, e ele tudo fará.",
     "Commit your way to the Lord;\ntrust in him and he will do this.", "Sl / Ps 37:5"),
    (5,  "16,75 km", "Seja forte e corajoso! Não se apavore,\npois o Senhor, o teu Deus, estará contigo.",
     "Be strong and courageous. Do not be afraid;\nthe Lord your God will be with you.", "Js / Jo 1:9"),
    (6,  "20,10 km", "Os que esperam no Senhor renovam as suas forças.\nVoam alto como águias.",
     "Those who hope in the Lord will renew their strength.\nThey will soar on wings like eagles.", "Is / Is 40:31"),
    (7,  "23,45 km", "Deus é o nosso refúgio e a nossa força,\nauxílio sempre presente na hora da angústia.",
     "God is our refuge and strength,\nan ever-present help in trouble.", "Sl / Ps 46:1"),
    (8,  "26,80 km", "Em todas estas coisas somos mais que vencedores\npor meio daquele que nos amou.",
     "In all these things we are more than conquerors\nthrough him who loved us.", "Rm / Ro 8:37"),
    (9,  "30,15 km", "A minha graça é suficiente para você,\npois o meu poder se aperfeiçoa na fraqueza.",
     "My grace is sufficient for you,\nfor my power is made perfect in weakness.", "2Co / 2Co 12:9"),
    (10, "33,50 km", "Ainda que eu ande pelo vale da sombra da morte,\nnão temerei mal nenhum, pois tu estás comigo.",
     "Even though I walk through the darkest valley,\nI will fear no evil, for you are with me.", "Sl / Ps 23:4"),
    (11, "36,85 km", "Sede fortes e corajosos. Não temais,\npois o Senhor, teu Deus, vai contigo.",
     "Be strong and courageous. Do not be afraid;\nthe Lord your God goes with you.", "Dt / Dt 31:6"),
    (12, "40,20 km", "Sede fortalecidos no Senhor\ne na força do seu poder.",
     "Be strong in the Lord\nand in his mighty power.", "Ef / Ep 6:10"),
    (13, "43,55 km", "O Senhor é a minha rocha,\na minha fortaleza e o meu libertador.",
     "The Lord is my rock,\nmy fortress and my deliverer.", "Sl / Ps 18:2"),
    (14, "46,90 km", "Não temas, porque eu sou contigo;\nnão te assombres, porque eu sou o teu Deus.",
     "Do not fear, for I am with you;\ndo not be dismayed, for I am your God.", "Is / Is 41:10"),
    (15, "50,25 km", "Corramos com perseverança\na corrida que nos está proposta.",
     "Let us run with perseverance\nthe race marked out for us.", "Hb / He 12:1"),
    (16, "53,60 km", "O Senhor dará força ao seu povo;\no Senhor abençoará o seu povo com a paz.",
     "The Lord gives strength to his people;\nthe Lord blesses his people with peace.", "Sl / Ps 29:11"),
    (17, "56,95 km", "Graças a Deus que nos dá a vitória\npor meio de nosso Senhor Jesus Cristo.",
     "Thanks be to God! He gives us the victory\nthrough our Lord Jesus Christ.", "1Co / 1Co 15:57"),
    (18, "60,30 km", "No mundo tereis aflições; mas tende bom ânimo,\neu venci o mundo.",
     "In this world you will have trouble.\nBut take heart! I have overcome the world.", "Jo / Jn 16:33"),
    (19, "64 km",    "O vencedor herdará estas coisas,\ne eu serei o seu Deus e ele será o meu filho.",
     "The one who is victorious will inherit all this,\nand I will be his God and he will be my son.", "Ap / Rv 21:7"),
]

# ─── Helper: wrap text ─────────────────────────────────────────────────────────
def draw_centered_text(c, text, cx, y, font, size, color=colors.black, line_height=None):
    c.setFont(font, size)
    c.setFillColor(color)
    if line_height is None:
        line_height = size * 1.4
    lines = text.split('\n')
    total_h = (len(lines) - 1) * line_height
    start_y = y + total_h / 2
    for line in lines:
        c.drawCentredString(cx, start_y, line)
        start_y -= line_height
    return len(lines) * line_height

# ══════════════════════════════════════════════════════════════════════════════
# 1 — WHITE + VERSES PDF
# ══════════════════════════════════════════════════════════════════════════════
def make_cartolina_pdf(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Desafio 64km — Cartões com Versículos")

    CARD_H = H / 3          # 3 cards per page
    per_page = 3

    for idx, lap in enumerate(laps):
        num, km, pt, en, ref = lap
        page_pos = idx % per_page
        if page_pos == 0 and idx > 0:
            c.showPage()

        top = H - page_pos * CARD_H
        bot = top - CARD_H
        mid = (top + bot) / 2
        cx  = W / 2

        # card border
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.setLineWidth(1)
        c.rect(0, bot, W, CARD_H, stroke=1, fill=0)

        if num == 19:
            # Full-page final card
            if page_pos != 0:
                c.showPage()
            c.setFillColorRGB(0.12, 0.52, 0.29)  # green
            c.rect(0, 0, W, H, stroke=0, fill=1)
            cx = W / 2
            mid = H / 2

            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(colors.white)
            c.drawCentredString(cx, H - 20*mm, "VOLTA FINAL")

            c.setFont("Helvetica-Bold", 96)
            c.setFillColor(colors.white)
            c.drawCentredString(cx, mid + 45*mm, "19")

            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(cx, mid + 22*mm, "64 km — FINISH!")

            # divider
            c.setStrokeColor(colors.white)
            c.setLineWidth(2)
            c.line(cx - 50*mm, mid + 15*mm, cx + 50*mm, mid + 15*mm)

            c.setFont("Helvetica-Bold", 13)
            c.setFillColor(colors.white)
            for i, line in enumerate(pt.split('\n')):
                c.drawCentredString(cx, mid + 5*mm - i*18, line)

            c.setFont("Helvetica-Oblique", 11)
            c.setFillColorRGB(1,1,1,0.8)
            for i, line in enumerate(en.split('\n')):
                c.drawCentredString(cx, mid - 12*mm - i*16, line)

            c.setFont("Helvetica-Bold", 9)
            c.setFillColorRGB(1,1,1,0.9)
            c.drawRightString(W - 15*mm, 15*mm, ref)
            c.showPage()
            continue

        # VOLTA label (top-left corner)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColorRGB(0.7, 0.7, 0.7)
        c.drawString(12*mm, top - 10*mm, "VOLTA")

        # Number
        c.setFont("Helvetica-Bold", 72)
        c.setFillColorRGB(0.07, 0.07, 0.07)
        c.drawCentredString(cx, mid + 22*mm, str(num))

        # km
        c.setFont("Helvetica-Bold", 13)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawCentredString(cx, mid + 7*mm, km)

        # divider line
        c.setStrokeColorRGB(0.6, 0.6, 0.6)
        c.setLineWidth(1)
        c.line(cx - 35*mm, mid + 3*mm, cx + 35*mm, mid + 3*mm)

        # PT verse
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        pt_lines = pt.split('\n')
        for i, line in enumerate(pt_lines):
            c.drawCentredString(cx, mid - 4*mm - i*14, line)

        # EN verse
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColorRGB(0.4, 0.4, 0.4)
        en_lines = en.split('\n')
        offset = len(pt_lines) * 14 + 6
        for i, line in enumerate(en_lines):
            c.drawCentredString(cx, mid - 4*mm - offset - i*13, line)

        # reference
        c.setFont("Helvetica-Bold", 7)
        c.setFillColorRGB(0.65, 0.65, 0.65)
        c.drawRightString(W - 12*mm, bot + 8*mm, ref)

    c.save()
    print(f"✅  Saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# 2 — DARK BLUE PDF
# ══════════════════════════════════════════════════════════════════════════════
BLUE = (0.051, 0.106, 0.431)   # #0d1b6e

def make_azul_pdf(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Desafio 64km — Cartões Azul")

    CARD_H = H / 3
    per_page = 3

    for idx, lap in enumerate(laps):
        num, km = lap[0], lap[1]
        page_pos = idx % per_page
        if page_pos == 0 and idx > 0:
            c.showPage()

        top = H - page_pos * CARD_H
        bot = top - CARD_H
        mid = (top + bot) / 2
        cx  = W / 2

        if num == 19:
            if page_pos != 0:
                c.showPage()
            # darker blue full page
            c.setFillColorRGB(0.027, 0.063, 0.314)
            c.rect(0, 0, W, H, stroke=0, fill=1)
            c.setFont("Helvetica-Bold", 110)
            c.setFillColor(colors.white)
            c.drawCentredString(W/2, H/2 + 10*mm, "19")
            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(W/2, H/2 - 18*mm, "64 km 🏆")
            c.showPage()
            continue

        # blue card background
        c.setFillColorRGB(*BLUE)
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.rect(0, bot, W, CARD_H, stroke=1, fill=1)

        # Number
        c.setFont("Helvetica-Bold", 80)
        c.setFillColor(colors.white)
        c.drawCentredString(cx, mid + 10*mm, str(num))

        # km
        c.setFont("Helvetica-Bold", 18)
        c.setFillColorRGB(1, 1, 1, 0.75)
        c.drawCentredString(cx, mid - 12*mm, km)

    c.save()
    print(f"✅  Saved: {path}")


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    make_cartolina_pdf(os.path.join(base, 'cartoes-voltas.pdf'))
    make_azul_pdf(os.path.join(base, 'cartoes-azul.pdf'))
    print("\nDone! Open the PDFs in the desafio-64km folder.")

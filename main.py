import os, re, json, base64, datetime, requests
from flask import Flask, request, jsonify

LOGO_B64 = "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"
open("logo_cenergy.png", "wb").write(base64.b64decode(LOGO_B64))

# ===== gerador (layout fixo) =====
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    LongTable, TableStyle, KeepTogether, Table
)

TEAL   = colors.HexColor("#042D32")
GREEN  = colors.HexColor("#7DB828")
GREEN_D = colors.HexColor("#5F9410")   # verde mais escuro p/ texto de ação
GREY   = colors.HexColor("#666666")
LGREY  = colors.HexColor("#999999")
CARD_BG = colors.HexColor("#F2F6EC")   # fundo claro esverdeado dos cards

RISK_COLORS = {
    "ALTO":      colors.HexColor("#C0392B"),
    "MÉDIO":     colors.HexColor("#E08A1E"),
    "BAIXO":     GREEN,
    "SEM RISCO": TEAL,
}

LOGO = "logo_cenergy.png"
LOGO_ASPECT = 5.663          # largura/altura do PNG recortado
LOGO_W = 150
LOGO_H = LOGO_W / LOGO_ASPECT

PAGE_W, PAGE_H = A4
MARGIN = 14 * mm

def _styles():
    s = {}
    s["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15,
                                textColor=TEAL, spaceAfter=4, leading=18)
    s["intro"] = ParagraphStyle("intro", fontName="Helvetica", fontSize=7.5,
                                textColor=GREY, leading=10, spaceAfter=2)
    s["block"] = ParagraphStyle("block", fontName="Helvetica-Bold", fontSize=11,
                                textColor=TEAL, spaceBefore=10, spaceAfter=3, leading=13)
    s["sub"]   = ParagraphStyle("sub", fontName="Helvetica", fontSize=7.5,
                                textColor=GREY, leading=10, spaceAfter=3)
    s["th"]    = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.5,
                                textColor=colors.white, leading=9)
    s["cell"]  = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.3,
                                textColor=colors.HexColor("#222222"), leading=9)
    s["cell_b"] = ParagraphStyle("cell_b", fontName="Helvetica", fontSize=7.3,
                                textColor=colors.HexColor("#222222"), leading=9)
    s["risk"]  = ParagraphStyle("risk", fontName="Helvetica-Bold", fontSize=7.3,
                                textColor=colors.white, alignment=TA_CENTER, leading=9)
    s["leitura"] = ParagraphStyle("leitura", fontName="Helvetica", fontSize=7.3,
                                textColor=colors.HexColor("#333333"), leading=9.5,
                                spaceBefore=3, spaceAfter=2)
    s["card_title"] = ParagraphStyle("card_title", fontName="Helvetica-Bold", fontSize=10,
                                textColor=GREEN_D, leading=12, spaceAfter=1)
    s["card_src"] = ParagraphStyle("card_src", fontName="Helvetica-Oblique", fontSize=7,
                                textColor=LGREY, leading=9, spaceAfter=3)
    s["card_body"] = ParagraphStyle("card_body", fontName="Helvetica", fontSize=8,
                                textColor=colors.HexColor("#222222"), leading=11, spaceAfter=2)
    return s

S = _styles()

def _link(texto, url, style_color="#5F9410"):
    if url:
        return f'<a href="{url}" color="{style_color}"><u>{texto}</u></a>'
    return texto

def _make_header_footer(header_right_top, header_right_sub, footer_left):
    def header_footer(canvas, doc):
        canvas.saveState()
        if os.path.exists(LOGO):
            canvas.drawImage(LOGO, MARGIN, PAGE_H - MARGIN - LOGO_H,
                             width=LOGO_W, height=LOGO_H, mask="auto",
                             preserveAspectRatio=True)
        canvas.setFillColor(TEAL)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN - 4, header_right_top)
        canvas.setFillColor(GREY)
        canvas.setFont("Helvetica", 7)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN - 14, header_right_sub)
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(1.4)
        y = PAGE_H - MARGIN - LOGO_H - 5
        canvas.line(MARGIN, y, PAGE_W - MARGIN, y)
        canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
        canvas.setLineWidth(0.6)
        canvas.line(MARGIN, MARGIN + 14, PAGE_W - MARGIN, MARGIN + 14)
        canvas.setFillColor(LGREY)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(MARGIN, MARGIN + 5, footer_left)
        canvas.drawRightString(PAGE_W - MARGIN, MARGIN + 5, f"Página {doc.page}")
        canvas.restoreState()
    return header_footer

def _doc(path, header_right_top, header_right_sub, footer_left):
    top_used = LOGO_H + 16
    frame = Frame(MARGIN, MARGIN + 18, PAGE_W - 2*MARGIN,
                  PAGE_H - 2*MARGIN - top_used - 18, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN + top_used, bottomMargin=MARGIN + 18)
    hf = _make_header_footer(header_right_top, header_right_sub, footer_left)
    doc.addPageTemplates([PageTemplate(id="t", frames=[frame],
                                       onPage=hf)])
    return doc

def _tabela_reputacao(bloco):
    col_w = [16, 68, 40, 300, 44, 49]
    head = [Paragraph(h, S["th"]) for h in ["#", "Canal", "Data",
            "O que foi dito (linguagem simples)", "Tom", "Risco"]]
    data = [head]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E2E2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("VALIGN", (-1, 1), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
    ]
    for i, r in enumerate(bloco["rows"], start=1):
        num, canal, data_, texto, tom, risco = r
        row = [Paragraph(str(num), S["cell"]),
               Paragraph(canal, S["cell"]),
               Paragraph(data_, S["cell"]),
               Paragraph(texto, S["cell"]),
               Paragraph(tom, S["cell"]),
               Paragraph(risco, S["risk"])]
        data.append(row)
        style.append(("BACKGROUND", (5, i), (5, i), RISK_COLORS.get(risco, GREY)))
    t = LongTable(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t

def _tabela_itens(bloco):
    col_w = [16, 94, 70, 150, 148, 47]
    head = [Paragraph(h, S["th"]) for h in ["#", "Título", "Fonte / Data",
            "Resumo (linguagem simples)", "Impacto e ação sugerida", "Risco"]]
    data = [head]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E2E2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("VALIGN", (-1, 1), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i, it in enumerate(bloco["rows"], start=1):
        titulo = Paragraph(_link(it["titulo"], it.get("url")), S["cell_b"])
        fonte = Paragraph(it["fonte"], S["cell"])
        resumo = Paragraph(it["resumo"], S["cell"])
        imp = it["impacto"]
        if it.get("acao"):
            imp += f'<br/><br/><font color="{GREEN_D.hexval()[2:]}"></font>'
            imp = it["impacto"] + f'<br/><br/><b><font color="#5F9410">&rarr; Ação:</font></b> ' \
                  f'<font color="#3E6B0E">{it["acao"]}</font>'
        impacto = Paragraph(imp, S["cell"])
        risco = Paragraph(it["risco"], S["risk"])
        data.append([Paragraph(str(i), S["cell"]), titulo, fonte, resumo, impacto, risco])
        style.append(("BACKGROUND", (5, i), (5, i), RISK_COLORS.get(it["risco"], GREY)))
    t = LongTable(data, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t

def gerar_operacional(d, out_path):
    doc = _doc(out_path, "Inteligência de Mercado", "Relatório ao Conselho",
               "Cenergy Brasil  •  Documento interno / confidencial")
    story = []
    story.append(Paragraph("Report de Inteligência de Mercado", S["title"]))
    story.append(Paragraph(d["intro"], S["intro"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Bloco 1 — Cenergy: menções diretas e reputação", S["block"]))
    story.append(Paragraph(d["bloco1"]["subtitle"], S["sub"]))
    story.append(_tabela_reputacao(d["bloco1"]))
    story.append(Paragraph("<b>Leitura do bloco:</b> " + d["bloco1"]["leitura"], S["leitura"]))

    story.append(Paragraph("Bloco 2 — Regulatório (ANEEL)", S["block"]))
    story.append(Paragraph(d["bloco2"]["subtitle"], S["sub"]))
    story.append(_tabela_itens(d["bloco2"]))

    story.append(Paragraph("Bloco 3 — Setor elétrico (foco em GD)", S["block"]))
    story.append(Paragraph(d["bloco3"]["subtitle"], S["sub"]))
    story.append(_tabela_itens(d["bloco3"]))

    story.append(Spacer(1, 10))
    bar = Table([[Paragraph('<font color="white"><b>RESUMO EXECUTIVO</b></font>',
                            ParagraphStyle("rx", fontSize=9, leading=12))]],
                colWidths=[PAGE_W - 2*MARGIN])
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL),
                             ("LEFTPADDING", (0, 0), (-1, -1), 8),
                             ("TOPPADDING", (0, 0), (-1, -1), 4),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    pts = []
    for lead, txt in d["resumo"]:
        pts.append(Paragraph(f"<b>{lead}</b> {txt}",
                   ParagraphStyle("pt", fontName="Helvetica", fontSize=8,
                                  leading=11, spaceAfter=3,
                                  textColor=colors.HexColor("#222222"))))
    box = Table([[pts]], colWidths=[PAGE_W - 2*MARGIN])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CFE0B8")),
                             ("LINEABOVE", (0, 0), (-1, 0), 0, colors.white),
                             ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FBFDF7")),
                             ("LEFTPADDING", (0, 0), (-1, -1), 10),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                             ("TOPPADDING", (0, 0), (-1, -1), 8),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(KeepTogether([bar, box]))
    doc.build(story)

def _card(n, item):
    titulo = Paragraph(f'{n}. ' + _link(item["titulo"], item.get("url")), S["card_title"])
    src = Paragraph(item["fonte"], S["card_src"])
    oque = Paragraph(f'<b>O que é:</b> {item["oque"]}', S["card_body"])
    opp = Paragraph(f'<b><font color="#5F9410">Oportunidade para a Cenergy:</font></b> '
                    f'{item["oportunidade"]}', S["card_body"])
    inner = Table([[ [titulo, src, oque, opp] ]], colWidths=[PAGE_W - 2*MARGIN - 6])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([inner, Spacer(1, 6)])

def gerar_cenergy(d, out_path):
    doc = _doc(out_path, "Monitor Cenergy", "Resumo de notícias",
               "Cenergy Brasil  •  Monitor Cenergy")
    story = [Paragraph("Monitor Cenergy", S["title"]),
             Paragraph(d["intro"], S["intro"]), Spacer(1, 6)]
    for i, item in enumerate(d["itens"], start=1):
        story.append(_card(i, item))
    doc.build(story)

# ===== endpoint =====
app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

@app.route("/", methods=["GET"])
def health():
    return "Cenergy render endpoint OK"

@app.route("/render", methods=["POST"])
def render():
    try:
        raw = request.get_data(as_text=True)
        payload = request.get_json(force=True, silent=True)
        if isinstance(payload, dict) and "operacional" in payload:
            data = payload
        else:
            txt = raw if isinstance(raw, str) else json.dumps(raw)
            data = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
        hoje = datetime.date.today().isoformat()
        op = "/tmp/Monitor Operacional - Cenergy Brasil - " + hoje + ".pdf"
        ce = "/tmp/Monitor Cenergy - Cenergy Brasil - " + hoje + ".pdf"
        gerar_operacional(data["operacional"], op)
        gerar_cenergy(data["cenergy"], ce)
        status = []
        for p in (op, ce):
            with open(p, "rb") as fh:
                r = requests.post(
                    "https://api.telegram.org/bot" + BOT_TOKEN + "/sendDocument",
                    data={"chat_id": CHAT_ID, "caption": os.path.basename(p)},
                    files={"document": (os.path.basename(p), fh, "application/pdf")},
                    timeout=60)
            status.append(r.status_code)
        return jsonify({"ok": True, "telegram": status})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

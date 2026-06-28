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


# ---- dados de exemplo p/ teste sem gastar credito ----
EXEMPLO_JSON = '{"operacional": {"intro": "Data de elaboração: <b>25 de junho de 2026</b>  |  Período monitorado: jan a jun/2026. Reúne (1) menções e reputação da Cenergy, (2) mudanças regulatórias da ANEEL e (3) movimentos do setor de geração distribuída (GD = energia gerada perto de quem consome). Cada item traz a data e o risco real para o negócio. <b>Os títulos sublinhados são clicáveis e abrem a fonte consultada.</b>", "bloco1": {"subtitle": "Busca por “Cenergy” em redes sociais, Google e Reclame Aqui. <b>Observação:</b> não foi localizada página da <b>Cenergy Brasil</b> no Reclame Aqui nem avaliações públicas no Google. Empresas de nome parecido (“Energy Brasil”, “Conergy”, “Cnergia”) <b>não</b> são a Cenergy e foram descartadas.", "rows": [[1, "Site / Blog oficial", "abr/2026", "A própria empresa explica o modelo: assume a conta junto à distribuidora, faz a troca de titularidade e cobra um boleto com desconto de <b>15% a 20%</b> sobre a tarifa. Material institucional, sem reclamação.", "Positivo", "SEM RISCO"], [2, "Instagram @cenergybrasil", "jun/2026", "Conta ativa. Promoções de Copa do Mundo em curso (20/06 a 19/07): “Energia que Torce Junto” (residencial) e “Sua Torcida Economiza” (síndicos/condomínios) sorteiam <b>Smart TVs, créditos na fatura e vouchers de combustível</b> no DF. Cadastro pelo WhatsApp. Tom comercial/agressivo.", "Neutro", "BAIXO"], [3, "X (Twitter) @CenergyBrasil", "—", "Perfil existe, mas o conteúdo não estava acessível na consulta. <b>Nenhuma menção relevante encontrada no período.</b>", "—", "SEM RISCO"], [4, "Google Reviews / Meu Negócio", "jun/2026", "<b>Nenhuma avaliação pública localizada</b> para a Cenergy Brasil. Sem nota média nem volume indexado. É um <b>ponto cego</b>: hoje não medimos a reputação no Google.", "—", "MÉDIO"], [5, "Reclame Aqui", "jun/2026", "<b>Nenhuma página da Cenergy Brasil localizada</b> no período. Sem reclamações novas, sem índice de resposta. Ausência de cadastro também é ponto cego de monitoramento.", "—", "MÉDIO"], [6, "LinkedIn / Facebook", "jun/2026", "Não localizado perfil corporativo ativo da Cenergy Brasil (“Cenergy Power” é empresa americana <b>diferente</b>). Nenhuma menção encontrada no período.", "Neutro", "BAIXO"]], "leitura": "não há crise de reputação visível, mas a Cenergy é praticamente invisível em Reclame Aqui e Google. Se um cliente reclamar de boleto ou desconto, hoje não temos como detectar e responder. <b><font color=\\"#5F9410\\">&rarr; Ação:</font></b> criar e reivindicar os perfis no <b>Google Meu Negócio</b> e no <b>Reclame Aqui</b>, com rotina de monitoramento e resposta às avaliações."}, "bloco2": {"subtitle": "Regras que definem quanto vale o crédito de energia e quanto custa a tarifa. É aqui que mora o maior risco para a receita.", "rows": [{"titulo": "Fio B sobe para 60% em 2026", "url": "https://canalsolar.com.br/", "risco": "ALTO", "fonte": "Lei 14.300/2022<br/>Canal Solar / PV Magazine<br/>jan/2026", "resumo": "O “Fio B” (parte da conta que paga fios e postes) deixa de ser compensado pelos créditos de forma crescente. Em 2026 chega a <b>60%</b> (era 45% em 2025) e sobe até 2028. Na prática, <b>cada crédito vale menos.</b>", "impacto": "<b>Reduz o valor do crédito</b> que abatemos na conta do cliente. Pressiona a margem de 15%: absorver a perda ou repassar e ficar menos competitivo.", "acao": "simular a perda de margem por distribuidora e definir um <b>piso de margem</b>; revisar a política de desconto e estudar cláusula de repasse parcial do Fio B."}, {"titulo": "Indefinição da compensação após 2029", "url": "https://canalsolar.com.br/", "risco": "ALTO", "fonte": "Canal Solar<br/>jan/2026", "resumo": "A ANEEL <b>ainda não definiu</b> como a energia injetada será remunerada a partir de 2029, quando o sistema atual deixa de valer para quem entrou após 2023.", "impacto": "Cria incerteza para contratos e precificação de <b>longo prazo</b>. Dificulta planejar receita e novas usinas.", "acao": "incluir <b>cláusula de revisão</b> nos contratos longos; acompanhar as consultas públicas da ANEEL e modelar cenários de receita pós-2029."}, {"titulo": "Lei 15.269/2025 — segurança p/ troca de titularidade", "url": "https://www.portalsolar.com.br/", "risco": "BAIXO", "fonte": "Portal Solar / Cescon<br/>nov/2025", "resumo": "Nova lei deu base legal mais clara para a troca de titularidade e reconheceu o armazenamento em baterias. A troca de titularidade é justamente o que a Cenergy faz.", "impacto": "<b>Positivo:</b> mais segurança ao modelo de assumir a conta do cliente. Reduz risco jurídico atual.", "acao": "validar os contratos atuais com o jurídico à luz da nova lei e <b>usar a segurança jurídica</b> como argumento de venda e retenção."}, {"titulo": "Veto: CDE não cobre subsídio da GD", "url": "https://www.simpleenergy.com.br/", "risco": "MÉDIO", "fonte": "Simple Energy / Gov<br/>fev/2026", "resumo": "O governo vetou usar um fundo setorial (CDE) para bancar o benefício da micro e minigeração. Os vetos ainda vão ao Congresso.", "impacto": "Sinaliza <b>pressão política contra subsídios</b> à GD. Se avançar, o incentivo que sustenta o desconto pode encolher.", "acao": "<b>monitorar a votação dos vetos</b> no Congresso; mapear a exposição da receita caso o subsídio caia e reforçar atuação via associação do setor (ABGD/ABSOLAR)."}, {"titulo": "Reajuste tarifário Neoenergia Brasília", "url": "https://www.gov.br/aneel/", "risco": "BAIXO", "fonte": "ANEEL (gov.br)<br/>vig. 22/10/2025", "resumo": "A ANEEL aprovou o reajuste anual da distribuidora do DF: efeito médio de <b>11,65%</b> (baixa tensão 10,88%; residencial 10,56%; alta tensão 13,82%), em vigor desde 22/10/2025. Tarifa mais alta = base de cálculo do nosso desconto maior.", "impacto": "<b>Misto:</b> tarifa maior aumenta o valor economizado/cobrado, mas encarece o boleto — atenção à inadimplência.", "acao": "reprecificar os boletos com o novo índice e comunicar o reajuste ao cliente de forma transparente para reduzir atrito."}, {"titulo": "Consulta Pública 009/2026: excedentes e possíveis cortes na GD", "url": "https://www.gov.br/aneel/", "risco": "MÉDIO", "fonte": "ANEEL / Canal Solar<br/>contrib. até 06/jun/2026", "resumo": "A ANEEL abriu consulta (já encerrada, em análise) sobre o tratamento de excedentes de energia e maior controle da rede. Inclui <b>fiscalização de sistemas ampliados sem autorização</b> (exclusão da compensação, cobrança retroativa e, em casos graves, <b>corte físico</b>) e instrumentos de coordenação ONS–distribuidoras.", "impacto": "Para operadores regulares como a Cenergy o efeito direto é baixo, mas sinaliza rede mais restritiva e fiscalização mais dura.", "acao": "<b>garantir que todas as usinas estejam homologadas</b> e dentro da potência autorizada; acompanhar o desfecho da consulta via associação."}, {"titulo": "ANEEL discute créditos de GD que expiram em 60 meses", "url": "https://www.pv-magazine.com/", "risco": "MÉDIO", "fonte": "ANEEL / PV Magazine<br/>contrib. até 15/jun/2026", "resumo": "Consulta (encerrada, em análise) sobre o tratamento dos <b>créditos não usados em 60 meses</b>, que expiram e passam a reverter “em prol da modicidade tarifária”. Define como esses créditos serão contabilizados e valorados.", "impacto": "Mexe no <b>insumo central da nossa receita</b> (os créditos). Tema a acompanhar; ainda sem resolução.", "acao": "revisar a <b>gestão de validade dos créditos</b> para minimizar expiração e contribuir na consulta via associação (ABGD/ABSOLAR)."}]}, "bloco3": {"subtitle": "Tendências de mercado, concorrência e comportamento do consumidor que afetam o modelo de desconto por assinatura.", "rows": [{"titulo": "Mercado solar deve recuar ~7% em 2026", "url": "https://canalsolar.com.br/previsao-da-energia-solar-em-2026/", "risco": "BAIXO", "fonte": "ABSOLAR / ABGD<br/>dez/2025 – jan/2026", "resumo": "A ABSOLAR projeta queda de ~7% na instalação de novos painéis em 2026 (2º ano de retração, por juros altos e entraves). Já a ABGD projeta a GD crescendo ~15%, chegando a ~50 GW. O modelo por assinatura segue, mas pode desacelerar pelo Fio B e pelos juros.", "impacto": "Captação mais difícil e crédito mais caro. Ainda assim, a <b>procura por desconto permanece</b> — favorável ao produto.", "acao": "focar em <b>retenção e eficiência de captação</b> (reduzir custo de aquisição) e priorizar regiões de tarifa alta, onde o desconto vende melhor."}, {"titulo": "Assinatura solar entra em fase de “maturidade”", "url": "https://canalsolar.com.br/", "risco": "MÉDIO", "fonte": "Canal Solar / ADELATAM<br/>mai/2026", "resumo": "O setor diz que a disputa virou <b>confiança, atendimento, crédito, inadimplência, churn</b> (cancelamento) e reputação. Fase “menos romântica e mais sofisticada”.", "impacto": "Atinge o <b>coração do modelo</b> de boleto. Exige gestão de inadimplência, atendimento e reputação — hoje um ponto fraco (Bloco 1).", "acao": "implantar <b>régua de cobrança</b>, análise de crédito na adesão e métricas de churn; estruturar canal de atendimento (SAC) e monitoramento de reputação."}, {"titulo": "Fio B acelera baterias e sistemas híbridos", "url": "https://www.pv-magazine.com/", "risco": "MÉDIO", "fonte": "PV Magazine<br/>jan/2026", "resumo": "Com o crédito valendo menos, concorrentes passam a oferecer baterias e soluções híbridas para compensar a perda.", "impacto": "Risco de a Cenergy ficar <b>defasada</b> se mantiver só o desconto simples. Oportunidade de estudar armazenamento.", "acao": "avaliar um <b>piloto de baterias (BESS)</b> e parcerias tecnológicas; montar roadmap de produto híbrido para não perder competitividade."}, {"titulo": "Conta de luz deve subir 8,6% em 2026", "url": "https://www.gov.br/aneel/", "risco": "BAIXO", "fonte": "ANEEL (boletim)<br/>jun/2026", "resumo": "A ANEEL projeta alta média de <b>8,6%</b> na conta de luz em 2026, acima da inflação (IPCA ~4,9%). Conta mais cara torna o desconto <b>mais atraente para vender</b>, mas aumenta o valor do boleto.", "impacto": "<b>Misto:</b> bom para captar; ruim para inadimplência, pois o boleto fica mais pesado.", "acao": "usar a <b>economia como mote de venda</b>, mas reforçar a análise de crédito e oferecer formas de pagamento para conter a inadimplência."}, {"titulo": "Distribuidoras negando conexão de novos sistemas", "url": "https://www.absolar.org.br/", "risco": "MÉDIO", "fonte": "ABSOLAR<br/>dez/2025", "resumo": "Crescem as negativas de conexão de novos sistemas de GD, alegando “inversão de fluxo” (rede sem capacidade de receber a energia).", "impacto": "Pode <b>dificultar a expansão</b> de novas usinas e a entrada de clientes em algumas áreas.", "acao": "<b>mapear a capacidade da rede por região</b> antes de prospectar e diversificar a localização das usinas para evitar gargalos de conexão."}]}, "resumo": [["1. Mais urgente:", "o Fio B subiu para 60% em 2026 — os créditos passam a valer menos e a margem de 15% fica sob pressão direta."], ["2. Decisão do conselho:", "definir como proteger a margem (absorver x repassar), preparar um plano para a indefinição pós-2029 e criar monitoramento de reputação — hoje a Cenergy não aparece no Reclame Aqui nem no Google."], ["3. Ameaça à receita:", "SIM. Fio B em alta + entrada do setor na fase de inadimplência/cancelamento atingem exatamente o modelo de boleto com desconto."], ["4. Sem crise de imagem aparente,", "mas o ponto cego de reputação precisa ser resolvido antes que vire problema."]]}, "cenergy": {"intro": "25 de junho de 2026. Um resumo das principais notícias do setor de energia solar e geração distribuída (energia gerada perto de quem consome), em linguagem simples. Cada item traz o título com link para a fonte, o que ele significa e onde está a oportunidade para o nosso negócio.", "itens": [{"titulo": "Conta de luz deve subir 8,6% em 2026, acima da inflação", "url": "https://www.gov.br/aneel/", "fonte": "ANEEL — boletim de jun/2026 | reajuste local da Neoenergia Brasília (DF): +11,65% desde out/2025", "oque": "A agência reguladora projeta que a conta de luz vai subir, em média, 8,6% no Brasil em 2026 — acima da inflação. No DF, nosso principal mercado, a distribuidora já teve reajuste de 11,65%.", "oportunidade": "Quanto mais cara a conta da distribuidora, <b>mais valioso fica o desconto que oferecemos</b>. É um cenário favorável para vendas e captação, especialmente no Distrito Federal — bom momento para reforçar a mensagem de economia."}, {"titulo": "ANEEL discute novas regras para a geração distribuída (Consultas Públicas)", "url": "https://www.gov.br/aneel/", "fonte": "ANEEL / Canal Solar — consultas encerradas em jun/2026, em análise", "oque": "A ANEEL conduziu duas consultas públicas (etapas em que o setor envia sugestões antes de novas regras): uma sobre o controle de excedentes e a fiscalização de sistemas irregulares, outra sobre os créditos de energia que vencem em 5 anos. São discussões em andamento, ainda sem decisão.", "oportunidade": "Regras mais firmes contra instalações irregulares <b>beneficiam quem opera certo, como a Cenergy</b>, e nivelam o jogo. É também a hora de ter voz no debate (via associação) e de reforçar a boa gestão dos créditos dos clientes."}, {"titulo": "Fio B chega a 60% em 2026 na geração distribuída", "url": "https://canalsolar.com.br/", "fonte": "Lei 14.300/2022 — Canal Solar — jan/2026", "oque": "O “Fio B” é a parte da conta que paga a rede (fios e postes). Pela lei de 2022, ele passa a ser cobrado de forma crescente sobre a energia solar injetada — em 2026 chega a 60%. Na prática, o crédito de energia rende um pouco menos.", "oportunidade": "A economia sobre os demais itens da conta <b>continua valendo integralmente</b>, então o desconto segue atraente. É também o gatilho para evoluirmos o produto — por exemplo, estudar baterias/armazenamento — e nos diferenciarmos pela eficiência na gestão dos créditos."}, {"titulo": "Reforma do setor elétrico (Lei 15.269/2025) dá segurança jurídica à troca de titularidade", "url": "https://www.portalsolar.com.br/", "fonte": "Portal Solar — nov/2025", "oque": "A nova lei do setor deixou mais claras as regras para a troca de titularidade da conta de luz (assumir a conta do cliente) e reconheceu oficialmente o armazenamento de energia em baterias.", "oportunidade": "Dá <b>respaldo legal ao coração do nosso modelo</b> — um ótimo argumento de confiança para clientes e parceiros. E abre caminho para, no futuro, oferecermos soluções com baterias."}, {"titulo": "Setor solar recua, mas a geração distribuída deve crescer ~15% em 2026", "url": "https://www.absolar.org.br/", "fonte": "ABSOLAR / ABGD — dez/2025 e jan/2026", "oque": "Enquanto a instalação total de painéis deve cair cerca de 7% em 2026 (juros altos e entraves), a associação da geração distribuída (ABGD) projeta que esse segmento — o nosso — cresça cerca de 15%, chegando a ~50 GW.", "oportunidade": "Estamos no <b>segmento mais resiliente</b> do mercado. Com parte dos concorrentes mais cautelosa, há espaço para a Cenergy ganhar participação e consolidar a marca."}, {"titulo": "Energia solar por assinatura entra em fase de maturidade", "url": "https://canalsolar.com.br/", "fonte": "Canal Solar / ADELATAM — mai/2026", "oque": "O setor avalia que a disputa deixou de ser só “conectar usinas” e passou a girar em torno de confiança, qualidade de atendimento e experiência do cliente. O Brasil aparece liderando esse próximo ciclo na América Latina.", "oportunidade": "Quem investir em <b>experiência do cliente e reputação sai na frente</b>. É a oportunidade de posicionar a Cenergy como referência de confiança — um diferencial que sustenta crescimento de longo prazo."}]}}'

def _enviar(op, ce):
    status = []
    for p in (op, ce):
        with open(p, "rb") as fh:
            r = requests.post(
                "https://api.telegram.org/bot" + BOT_TOKEN + "/sendDocument",
                data={"chat_id": CHAT_ID, "caption": os.path.basename(p)},
                files={"document": (os.path.basename(p), fh, "application/pdf")},
                timeout=60)
        status.append(r.status_code)
    return status

@app.route("/test", methods=["GET"])
def test():
    try:
        data = json.loads(EXEMPLO_JSON)
        hoje = datetime.date.today().isoformat()
        op = "/tmp/Monitor Operacional - Cenergy Brasil - " + hoje + ".pdf"
        ce = "/tmp/Monitor Cenergy - Cenergy Brasil - " + hoje + ".pdf"
        gerar_operacional(data["operacional"], op)
        gerar_cenergy(data["cenergy"], ce)
        st = _enviar(op, ce)
        return jsonify({"ok": True, "telegram": st, "msg": "Teste enviado ao grupo. Veja o Telegram."})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

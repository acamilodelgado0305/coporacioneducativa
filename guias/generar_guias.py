# -*- coding: utf-8 -*-
"""
Genera las guías de estudio en PDF que se descargan gratis desde las landings
(antes de pagar):

    guias/guia-manipulacion-de-alimentos.pdf
    guias/guia-auxiliar-de-bodega-y-logistica.pdf

El texto de cada guía está en contenido_manipulacion.py y contenido_bodega.py.
Para corregir o ampliar una guía, edita ese archivo y vuelve a generar:

    python guias/generar_guias.py

Requiere: pip install reportlab
"""
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer, Table)
from reportlab.platypus.tableofcontents import TableOfContents

import contenido_bodega
import contenido_manipulacion

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, 'logo_guia.png')

W, H = A4
MARGIN = 54
CW = W - 2 * MARGIN  # ancho útil

# Paleta de la marca (la misma de las landings)
BLUE = HexColor('#0158AD')
BLUE_DARK = HexColor('#013d7a')
BLUE_MID = HexColor('#0d6bc7')
BLUE_SOFT = HexColor('#bfdbfe')
LIGHT = HexColor('#eff6ff')
YELLOW = HexColor('#FBC13D')
DARK = HexColor('#0f172a')
INK = HexColor('#334155')
MUTED = HexColor('#64748b')
LINE = HexColor('#e2e8f0')
SOFT = HexColor('#f8fafc')
AMBER = HexColor('#b45309')
AMBER_BG = HexColor('#fffbeb')
GREEN = HexColor('#15803d')
GREEN_BG = HexColor('#f0fdf4')


# ── Estilos de texto ─────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=10.5, leading=15.5, textColor=INK)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    'body': S('body', spaceAfter=7),
    'small': S('small', fontSize=8.5, leading=12, textColor=MUTED, spaceAfter=6),
    'h2': S('h2', fontName='Helvetica-Bold', fontSize=13.5, leading=18, textColor=DARK, spaceBefore=12, spaceAfter=6),
    'h3': S('h3', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=BLUE, spaceBefore=8, spaceAfter=4),
    'bullet': S('bullet', leftIndent=15, bulletIndent=3, spaceAfter=3.5, bulletColor=BLUE, bulletFontName='Helvetica-Bold'),
    'cell': S('cell', fontSize=9.2, leading=12.6),
    'cell_b': S('cell_b', fontName='Helvetica-Bold', fontSize=9.2, leading=12.6, textColor=DARK),
    'cell_head': S('cell_head', fontName='Helvetica-Bold', fontSize=9.2, leading=12.6, textColor=white),
    'ch_label': S('ch_label', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=YELLOW),
    'ch_title': S('ch_title', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=white),
    'ch_intro': S('ch_intro', fontSize=10.5, leading=15, textColor=BLUE_SOFT),
    'step_t': S('step_t', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=DARK),
    'step_d': S('step_d', fontSize=9.6, leading=13.6, spaceBefore=1),
    'formula': S('formula', fontName='Helvetica-Bold', fontSize=15, leading=20, textColor=BLUE, alignment=TA_CENTER),
    'formula_d': S('formula_d', fontSize=9.6, leading=13.6),
    'q': S('q', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=DARK, spaceBefore=6, spaceAfter=2),
    'opt': S('opt', fontSize=9.6, leading=13.4, leftIndent=14),
    'toc': S('toc', fontSize=11, leading=22, textColor=DARK),
    'flow': S('flow', fontName='Helvetica-Bold', fontSize=8.6, leading=11, textColor=BLUE_DARK, alignment=TA_CENTER),
    'flow_arrow': S('flow_arrow', fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=YELLOW, alignment=TA_CENTER),
    'cta_title': S('cta_title', fontName='Helvetica-Bold', fontSize=22, leading=27, textColor=white),
    'cta_body': S('cta_body', fontSize=11, leading=16, textColor=white, spaceAfter=6),
    'cta_bullet': S('cta_bullet', fontSize=10.5, leading=15, textColor=white, leftIndent=15, bulletIndent=3,
                    bulletColor=YELLOW, bulletFontName='Helvetica-Bold', spaceAfter=3),
    'cover_title': S('cover_title', fontName='Helvetica-Bold', fontSize=36, leading=40, textColor=white),
    'cover_sub': S('cover_sub', fontSize=13, leading=18, textColor=BLUE_SOFT),
    'cover_box': S('cover_box', fontSize=10, leading=14.5, textColor=INK),
    'feat_t': S('feat_t', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=DARK, alignment=TA_CENTER),
    'feat_d': S('feat_d', fontSize=8.6, leading=11.5, textColor=MUTED, alignment=TA_CENTER),
}


# ── Piezas gráficas pequeñas ─────────────────────────────────────
class NumBadge(Flowable):
    """Círculo azul con el número del paso."""
    def __init__(self, n, size=20):
        super().__init__()
        self.n, self.size = n, size

    def wrap(self, aw, ah):
        return self.size, self.size

    def draw(self):
        r = self.size / 2
        self.canv.setFillColor(BLUE)
        self.canv.circle(r, r, r, fill=1, stroke=0)
        self.canv.setFillColor(white)
        self.canv.setFont('Helvetica-Bold', 10)
        self.canv.drawCentredString(r, r - 3.6, str(self.n))


class CheckBox(Flowable):
    """Casilla vacía para las listas de chequeo."""
    def wrap(self, aw, ah):
        return 12, 12

    def draw(self):
        self.canv.setStrokeColor(BLUE)
        self.canv.setLineWidth(1.2)
        self.canv.roundRect(0, 0, 11, 11, 2, fill=0, stroke=1)


# ── Bloques de contenido ─────────────────────────────────────────
def chapter_block(num, title, intro, key):
    t = Table([[Paragraph('CAPÍTULO %d' % num, ST['ch_label'])],
               [Paragraph(title, ST['ch_title'])],
               [Paragraph(intro, ST['ch_intro'])]], colWidths=[CW])
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 20), ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, 0), 16), ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 2), ('BOTTOMPADDING', (0, 1), (-1, 1), 6),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 16),
        ('LINEBELOW', (0, -1), (-1, -1), 4, YELLOW),
    ])
    t.toc_title = '%d. %s' % (num, title)
    t.toc_key = key
    return [CondPageBreak(260), t, Spacer(1, 12)]


def section_block(title, key, intro=None):
    """Encabezado de secciones finales (repaso, glosario) que también va al índice."""
    rows = [[Paragraph(title, ST['ch_title'])]]
    if intro:
        rows.append([Paragraph(intro, ST['ch_intro'])])
    t = Table(rows, colWidths=[CW])
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_DARK),
        ('LEFTPADDING', (0, 0), (-1, -1), 20), ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, 0), 14), ('BOTTOMPADDING', (0, -1), (-1, -1), 14),
        ('LINEBELOW', (0, -1), (-1, -1), 4, YELLOW),
    ])
    t.toc_title = title
    t.toc_key = key
    return [t, Spacer(1, 12)]


def bullets(items, style='bullet'):
    return [Paragraph(it, ST[style], bulletText='•') for it in items]


def steps(items):
    rows = []
    for i, it in enumerate(items, 1):
        title, desc = (it, None) if isinstance(it, str) else it
        cell = [Paragraph(title, ST['step_t'])]
        if desc:
            cell.append(Paragraph(desc, ST['step_d']))
        rows.append([NumBadge(i), cell])
    t = Table(rows, colWidths=[30, CW - 30])
    t.setStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, LINE),
    ])
    return [t, Spacer(1, 8)]


CALLOUTS = {
    'info': (LIGHT, BLUE, 'RECUERDA'),
    'warn': (AMBER_BG, AMBER, 'ATENCIÓN'),
    'key': (GREEN_BG, GREEN, 'DATO CLAVE'),
}


def callout(kind, title, text):
    bg, accent, label = CALLOUTS[kind]
    head = ParagraphStyle('ct', parent=ST['step_t'], textColor=accent)
    lab = ParagraphStyle('cl', parent=ST['ch_label'], textColor=accent, fontSize=7.8)
    content = [Paragraph(label, lab), Paragraph(title, head), Paragraph(text, ST['step_d'])]
    t = Table([[content]], colWidths=[CW])
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, accent),
        ('LEFTPADDING', (0, 0), (-1, -1), 14), ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, -1), 11),
    ])
    return [Spacer(1, 4), KeepTogether(t), Spacer(1, 10)]


def data_table(header, rows, ratios=None, first_bold=True):
    n = len(header)
    ratios = ratios or [1] * n
    widths = [CW * r / sum(ratios) for r in ratios]
    data = [[Paragraph(h, ST['cell_head']) for h in header]]
    for r in rows:
        data.append([Paragraph(c, ST['cell_b'] if (first_bold and j == 0) else ST['cell']) for j, c in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, SOFT]),
        ('GRID', (0, 0), (-1, -1), 0.5, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    return [Spacer(1, 2), t, Spacer(1, 10)]


def color_table(rows):
    """Tabla del código de colores de residuos: la primera columna va pintada."""
    data = [[Paragraph(h, ST['cell_head']) for h in ('Caneca', 'Tipo de residuo', 'Ejemplos')]]
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('GRID', (0, 0), (-1, -1), 0.5, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]
    for i, (hexcol, text_hex, label, kind, examples) in enumerate(rows, 1):
        lab = ParagraphStyle('c%d' % i, parent=ST['cell_b'], textColor=HexColor(text_hex), alignment=TA_CENTER)
        data.append([Paragraph(label, lab), Paragraph(kind, ST['cell_b']), Paragraph(examples, ST['cell'])])
        style.append(('BACKGROUND', (0, i), (0, i), HexColor(hexcol)))
    t = Table(data, colWidths=[CW * 0.18, CW * 0.27, CW * 0.55])
    t.setStyle(style)
    return [Spacer(1, 2), t, Spacer(1, 10)]


def checklist(title, items):
    rows = [[Paragraph(title, ST['cell_head']), '']]
    for it in items:
        rows.append([CheckBox(), Paragraph(it, ST['cell'])])
    t = Table(rows, colWidths=[26, CW - 26])
    t.setStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, BLUE),
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, BLUE_SOFT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    return [Spacer(1, 4), KeepTogether(t), Spacer(1, 12)]


def formula(main, lines):
    content = [Paragraph(main, ST['formula']), Spacer(1, 6)] + [Paragraph(l, ST['formula_d']) for l in lines]
    t = Table([[content]], colWidths=[CW])
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 16), ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 12), ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ])
    return [Spacer(1, 4), KeepTogether(t), Spacer(1, 12)]


def flow(labels):
    """Cadena de pasos en una fila: A » B » C."""
    cells, widths = [], []
    box_w = (CW - 14 * (len(labels) - 1)) / len(labels)
    for i, lab in enumerate(labels):
        if i:
            cells.append(Paragraph('»', ST['flow_arrow']))
            widths.append(14)
        cells.append(Paragraph(lab, ST['flow']))
        widths.append(box_w)
    t = Table([cells], colWidths=widths, rowHeights=[40])
    style = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
             ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2)]
    for i in range(0, len(cells), 2):
        style += [('BACKGROUND', (i, 0), (i, 0), LIGHT), ('BOX', (i, 0), (i, 0), 0.8, BLUE_SOFT)]
    t.setStyle(style)
    return [Spacer(1, 4), t, Spacer(1, 12)]


def rack(aisle, cols, levels, hl_col, hl_level):
    """Dibujo de un rack con la casilla marcada (ej.: A-03-2)."""
    head = ParagraphStyle('rk', parent=ST['cell_b'], alignment=TA_CENTER)
    data = [[Paragraph('Pasillo %s' % aisle, ST['cell_head'])] + [Paragraph('Rack %02d' % c, ST['cell_head']) for c in range(1, cols + 1)]]
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), BLUE),
        ('GRID', (0, 0), (-1, -1), 0.8, BLUE_SOFT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 9), ('BOTTOMPADDING', (0, 1), (-1, -1), 9),
    ]
    for r, lvl in enumerate(range(levels, 0, -1), 1):
        row = [Paragraph('Nivel %d' % lvl, head)]
        for c in range(1, cols + 1):
            if c == hl_col and lvl == hl_level:
                row.append(Paragraph('%s-%02d-%d' % (aisle, c, lvl), head))
                style.append(('BACKGROUND', (c, r), (c, r), YELLOW))
            else:
                row.append('')
        data.append(row)
        style.append(('BACKGROUND', (0, r), (0, r), LIGHT))
    t = Table(data, colWidths=[CW * 0.2] + [CW * 0.8 / cols] * cols)
    t.setStyle(style)
    return [Spacer(1, 4), KeepTogether(t), Spacer(1, 10)]


def quiz(questions):
    out = []
    for i, (q, opts, ans) in enumerate(questions, 1):
        block = [Paragraph('%d. %s' % (i, q), ST['q'])]
        block += [Paragraph('%s) %s' % ('abc'[j], o), ST['opt']) for j, o in enumerate(opts)]
        out.append(KeepTogether(block))
    # Clave de respuestas: filas de 5
    out += [Spacer(1, 14), Paragraph('Respuestas', ST['h2'])]
    keys = ['%d. %s' % (i, 'abc'[a]) for i, (_, _, a) in enumerate(questions, 1)]
    rows = [keys[i:i + 5] + [''] * (5 - len(keys[i:i + 5])) for i in range(0, len(keys), 5)]
    t = Table([[Paragraph(k, ST['cell_b']) for k in r] for r in rows], colWidths=[CW / 5] * 5)
    t.setStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, LINE),
        ('BACKGROUND', (0, 0), (-1, -1), SOFT),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ])
    out += [t, Spacer(1, 6),
            Paragraph('Si fallaste alguna, vuelve al capítulo correspondiente y repásalo antes del examen.', ST['small'])]
    return out


def glossary(items):
    return [Paragraph('<b>%s:</b> %s' % (term, d), ST['body']) for term, d in items]


def cta_page(g):
    content = [Paragraph(g['cta_title'], ST['cta_title']), Spacer(1, 8)]
    content += [Paragraph(p, ST['cta_body']) for p in g['cta_text']]
    content += [Spacer(1, 4)] + bullets(g['cta_bullets'], 'cta_bullet')
    content += [Spacer(1, 10), Paragraph(
        '¿Tienes dudas? Escríbenos por WhatsApp al <b>310 794 1580</b>.', ST['cta_body'])]
    t = Table([[content]], colWidths=[CW])
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE),
        ('LINEBELOW', (0, 0), (-1, -1), 5, YELLOW),
        ('LEFTPADDING', (0, 0), (-1, -1), 24), ('RIGHTPADDING', (0, 0), (-1, -1), 24),
        ('TOPPADDING', (0, 0), (-1, -1), 24), ('BOTTOMPADDING', (0, 0), (-1, -1), 24),
    ])
    disclaimer = ('<b>Aviso:</b> esta guía es material educativo de apoyo elaborado por CertiTec Colombia. '
                  'No reemplaza el texto oficial de las normas citadas ni los procedimientos internos de tu empresa. '
                  'Consulta siempre las normas vigentes. CertiTec Colombia es la plataforma donde te inscribes y pagas; '
                  'el certificado lo emite y firma Alianza Capacitarte.')
    return [PageBreak(), Spacer(1, 40), t, Spacer(1, 28), Paragraph(disclaimer, ST['small'])]


def render(blocks, key_prefix):
    story, ch = [], 0
    for b in blocks:
        kind = b[0]
        if kind == 'chapter':
            ch += 1
            story += chapter_block(ch, b[1], b[2], '%s-ch%d' % (key_prefix, ch))
        elif kind == 'section':
            story += [PageBreak()] + section_block(b[1], '%s-%s' % (key_prefix, b[2]), b[3] if len(b) > 3 else None)
        elif kind == 'h2':
            story.append(CondPageBreak(90))
            story.append(Paragraph(b[1], ST['h2']))
        elif kind == 'h3':
            story.append(Paragraph(b[1], ST['h3']))
        elif kind == 'p':
            story.append(Paragraph(b[1], ST['body']))
        elif kind == 'small':
            story.append(Paragraph(b[1], ST['small']))
        elif kind == 'bullets':
            story += bullets(b[1]) + [Spacer(1, 5)]
        elif kind == 'steps':
            story += steps(b[1])
        elif kind == 'callout':
            story += callout(b[1], b[2], b[3])
        elif kind == 'table':
            story += data_table(b[1], b[2], b[3] if len(b) > 3 else None)
        elif kind == 'colors':
            story += color_table(b[1])
        elif kind == 'checklist':
            story += checklist(b[1], b[2])
        elif kind == 'formula':
            story += formula(b[1], b[2])
        elif kind == 'flow':
            story += flow(b[1])
        elif kind == 'rack':
            story += rack(*b[1:])
        elif kind == 'quiz':
            story += quiz(b[1])
        elif kind == 'glossary':
            story += glossary(b[1])
        else:
            raise ValueError('Bloque desconocido: %s' % kind)
    return story


# ── Documento ────────────────────────────────────────────────────
class GuideDoc(BaseDocTemplate):
    def __init__(self, path, g):
        super().__init__(path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=64, bottomMargin=60,
                         title='Guía de estudio: ' + g['course'], author='CertiTec Colombia',
                         subject=g['subtitle'], creator='CertiTec Colombia', keywords=g['keywords'])
        self.g = g
        cover = Frame(0, 0, W, H, id='cover', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        body = Frame(MARGIN, 60, CW, H - 124, id='body', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate('cover', [cover], onPage=draw_cover),
                               PageTemplate('content', [body], onPage=draw_content)])

    def afterFlowable(self, f):
        title = getattr(f, 'toc_title', None)
        if title:
            self.canv.bookmarkPage(f.toc_key)
            self.canv.addOutlineEntry(title, f.toc_key, level=0, closed=False)
            self.notify('TOCEntry', (0, title, self.page, f.toc_key))


def draw_content(canv, doc):
    canv.saveState()
    canv.setFillColor(BLUE)
    canv.rect(0, H - 6, W, 6, fill=1, stroke=0)
    canv.setFont('Helvetica-Bold', 8)
    canv.drawString(MARGIN, H - 34, 'CertiTec Colombia')
    canv.setFont('Helvetica', 8)
    canv.setFillColor(MUTED)
    canv.drawRightString(W - MARGIN, H - 34, 'Guía de estudio · ' + doc.g['course'])
    canv.setStrokeColor(LINE)
    canv.setLineWidth(0.6)
    canv.line(MARGIN, H - 42, W - MARGIN, H - 42)
    canv.line(MARGIN, 44, W - MARGIN, 44)
    canv.drawString(MARGIN, 30, 'Material de estudio gratuito · Certificado emitido y firmado por Alianza Capacitarte')
    canv.setFont('Helvetica-Bold', 8)
    canv.setFillColor(BLUE)
    canv.drawRightString(W - MARGIN, 30, str(doc.page))
    canv.restoreState()


def draw_cover(canv, doc):
    g = doc.g
    top = H * 0.60
    canv.saveState()

    # Bloque azul con círculos decorativos recortados
    canv.setFillColor(BLUE)
    canv.rect(0, H - top, W, top, fill=1, stroke=0)
    canv.saveState()
    clip = canv.beginPath()
    clip.rect(0, H - top, W, top)
    canv.clipPath(clip, stroke=0, fill=0)
    canv.setFillColor(BLUE_MID)
    canv.circle(W - 30, H - 70, 170, fill=1, stroke=0)
    canv.setFillColor(BLUE_DARK)
    canv.circle(W + 10, H - top - 20, 140, fill=1, stroke=0)
    canv.restoreState()
    canv.setFillColor(YELLOW)
    canv.rect(0, H - top - 8, W, 8, fill=1, stroke=0)

    # Marca
    canv.setFillColor(white)
    canv.circle(MARGIN + 26, H - 72, 26, fill=1, stroke=0)
    canv.drawImage(LOGO, MARGIN + 6, H - 72 - 16, 40, 32, mask='auto')
    canv.setFont('Helvetica-Bold', 15)
    canv.drawString(MARGIN + 64, H - 68, 'CertiTec Colombia')
    canv.setFont('Helvetica', 9)
    canv.setFillColor(BLUE_SOFT)
    canv.drawString(MARGIN + 64, H - 82, 'Formación virtual · Certificaciones laborales')

    # Título
    y = H - 190
    canv.setFont('Helvetica-Bold', 11)
    canv.setFillColor(YELLOW)
    canv.drawString(MARGIN, y, 'GUÍA DE ESTUDIO')
    p = Paragraph(g['cover_title'], ST['cover_title'])
    _, h = p.wrap(CW - 40, 300)
    y -= 14 + h
    p.drawOn(canv, MARGIN, y)
    p = Paragraph(g['subtitle'], ST['cover_sub'])
    _, h = p.wrap(CW - 60, 200)
    y -= 14 + h
    p.drawOn(canv, MARGIN, y)

    # Etiquetas
    x, y = MARGIN, y - 38
    canv.setFont('Helvetica-Bold', 9)
    for chip in g['chips']:
        w = canv.stringWidth(chip, 'Helvetica-Bold', 9) + 22
        canv.setFillColor(BLUE_DARK)
        canv.roundRect(x, y, w, 22, 11, fill=1, stroke=0)
        canv.setFillColor(white)
        canv.drawString(x + 11, y + 7.5, chip)
        x += w + 8

    # Tres destacados en la parte blanca
    feats = [[Paragraph(t, ST['feat_t']), Spacer(1, 3), Paragraph(d, ST['feat_d'])] for t, d in g['features']]
    t = Table([feats], colWidths=[(CW - 20) / 3] * 3)
    t.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SOFT),
        ('BOX', (0, 0), (0, 0), 0.6, LINE), ('BOX', (1, 0), (1, 0), 0.6, LINE), ('BOX', (2, 0), (2, 0), 0.6, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 12), ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])
    _, h = t.wrap(CW, 200)
    fy = H - top - 40 - h
    t.drawOn(canv, MARGIN, fy)

    p = Paragraph(g['cover_note'], ST['cover_box'])
    _, h = p.wrap(CW, 200)
    p.drawOn(canv, MARGIN, fy - 22 - h)

    # Pie
    canv.setStrokeColor(LINE)
    canv.line(MARGIN, 66, W - MARGIN, 66)
    canv.setFont('Helvetica', 8.5)
    canv.setFillColor(MUTED)
    canv.drawString(MARGIN, 50, 'CertiTec Colombia es la plataforma donde te inscribes y pagas.')
    canv.drawString(MARGIN, 38, 'Tu certificado lo emite y firma Alianza Capacitarte.')
    canv.setFont('Helvetica-Bold', 8.5)
    canv.setFillColor(BLUE)
    canv.drawRightString(W - MARGIN, 50, 'Soporte por WhatsApp')
    canv.drawRightString(W - MARGIN, 38, '310 794 1580')
    canv.restoreState()


def build(g, filename):
    path = os.path.join(HERE, filename)
    doc = GuideDoc(path, g)

    toc = TableOfContents()
    toc.levelStyles = [ST['toc']]
    toc.dotsMinLevel = 0

    story = [Spacer(1, 1), NextPageTemplate('content'), PageBreak(),
             Paragraph('Contenido', ST['h2']), Spacer(1, 4), toc, Spacer(1, 16)]
    story += callout('info', 'Cómo usar esta guía', g['how_to'])
    story += [PageBreak()]
    story += render(g['blocks'], g['key'])
    story += cta_page(g)

    doc.multiBuild(story)
    print('OK', path, '%.0f KB' % (os.path.getsize(path) / 1024))


def check_charset(obj, where=''):
    """Las fuentes estándar del PDF (Helvetica) solo traen caracteres Windows-1252:
    cualquier otro símbolo saldría como un cuadro negro."""
    if isinstance(obj, str):
        try:
            obj.encode('cp1252')
        except UnicodeEncodeError as e:
            raise SystemExit('Carácter no soportado en %s: %r' % (where, obj[max(0, e.start - 20):e.end + 20]))
    elif isinstance(obj, (list, tuple)):
        for i, o in enumerate(obj):
            check_charset(o, where)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            check_charset(v, k)


if __name__ == '__main__':
    for mod, name in ((contenido_manipulacion, 'guia-manipulacion-de-alimentos.pdf'),
                      (contenido_bodega, 'guia-auxiliar-de-bodega-y-logistica.pdf')):
        check_charset(mod.GUIA)
        build(mod.GUIA, name)

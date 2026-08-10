#!/usr/bin/env python3
"""
pdf_framework.py — The Ivy League Academic Monograph PDF Engine.

A professional, institutional-grade document framework in the tradition of
Ivy League research monographs and classified technical briefings:

  * US Letter, serif body (Times), small-caps masthead (Helvetica)
  * Full-bleed cover with real institutional logos and double-rule frame
  * Document-control page + auto-generated Table of Contents (real page numbers)
  * Running headers/footers with volume codes and classification bands
  * "KEY INSIGHT" call-out boxes, framed figures with source credits
  * References, glossary, timeline appendices, back-cover distribution notice
  * Diagonal classified watermark on body pages
  * Complete PDF metadata (title, author, subject, keywords, dates)

All content is passed in as structured data; the Table of Contents is built
from the *same* section list used for headings, so TOC and body always match.
"""
import os
from datetime import datetime, timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, Color, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether,
    HRFlowable, Frame, PageTemplate, BaseDocTemplate, NextPageTemplate,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas as pdfcanvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
ASSETS = os.path.join(ROOT, "assets")

PAGE_W, PAGE_H = letter  # 612 x 792
MARGIN = 0.9 * inch
W = PAGE_W - 2 * MARGIN  # usable width


def _c(hexstr):
    return HexColor(hexstr)


# ----------------------------------------------------------------------------
# Colour palettes — official institutional colours
# ----------------------------------------------------------------------------
UNIVERSITIES = {
    "Harvard University":   {"primary": "#A51C30", "accent": "#C4A265", "grey": "#5A5A5A"},
    "Yale University":      {"primary": "#00356B", "accent": "#C8A951", "grey": "#5A5A5A"},
    "Princeton University": {"primary": "#E87722", "accent": "#1E1E1E", "grey": "#5A5A5A"},
    "Brown University":     {"primary": "#4E3629", "accent": "#C41E3A", "grey": "#5A5A5A"},
    "Columbia University":  {"primary": "#012169", "accent": "#75AADB", "grey": "#5A5A5A"},
    "Cornell University":   {"primary": "#B31B1B", "accent": "#222222", "grey": "#5A5A5A"},
    "Dartmouth College":    {"primary": "#00693E", "accent": "#B5A36A", "grey": "#5A5A5A"},
    "University of Pennsylvania": {"primary": "#990000", "accent": "#011F5B", "grey": "#5A5A5A"},
    "Massachusetts Institute of Technology": {"primary": "#A31F34", "accent": "#8A8B8C", "grey": "#5A5A5A"},
    "Stanford University":  {"primary": "#8C1515", "accent": "#B3A369", "grey": "#5A5A5A"},
    "University of Oxford": {"primary": "#002147", "accent": "#C4A265", "grey": "#5A5A5A"},
    "University of Cambridge": {"primary": "#003366", "accent": "#A3C1AD", "grey": "#5A5A5A"},
}

CLASSIFICATIONS = [
    "TOP SECRET // SPECIAL ACCESS REQUIRED",
    "SECRET // NOFORN",
    "TOP SECRET // ORCON",
    "CONFIDENTIAL // LIMITED DISTRIBUTION",
    "SECRET // EYES ONLY",
    "TOP SECRET // SCI",
]


# ----------------------------------------------------------------------------
# Page decoration helpers
# ----------------------------------------------------------------------------
class IvyMonograph(BaseDocTemplate):
    """Two-pass document builder with cover / control / body / back templates."""

    def __init__(self, filename, spec, **kw):
        self.spec = spec
        self._toc = None
        super().__init__(filename, pagesize=letter,
                         leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=0.85 * inch, bottomMargin=0.8 * inch,
                         title=spec["title"],
                         author=spec.get("author", "Office of Advanced Research"),
                         subject=spec.get("subject", "Artificial Intelligence Research Monograph"),
                         keywords=spec.get("keywords", ""),
                         creator="Ivy League Academic Press — Monograph Production Service",
                         producer="IvyLeagueMonograph 2.0 / ReportLab",
                         **kw)
        self._build_templates()

    def afterFlowable(self, flowable):
        """Register section headings in the Table of Contents with real page numbers."""
        try:
            if flowable.__class__.__name__ == "Paragraph" and flowable.style.name == "SectionHead":
                text = flowable.getPlainText()
                key = "sec-%d-%d" % (self.page, abs(hash(text)) % 10**9)
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (0, text, self.page, key))
        except Exception:
            pass

    # -- page geometry helpers ------------------------------------------------
    def _body_frame(self):
        return Frame(MARGIN, 0.8 * inch, W, PAGE_H - 0.85 * inch - 0.8 * inch,
                     id="body", leftPadding=0, rightPadding=0, topPadding=6, bottomPadding=6)

    def _cover_frame(self):
        return Frame(0.55 * inch, 0.55 * inch, PAGE_W - 1.1 * inch, PAGE_H - 1.1 * inch,
                     id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def _build_templates(self):
        cover = PageTemplate(id="Cover", frames=[self._cover_frame()],
                             onPage=self._draw_cover_bg)
        control = PageTemplate(id="Control", frames=[self._body_frame()],
                               onPage=self._draw_control_bg)
        body = PageTemplate(id="Body", frames=[self._body_frame()],
                            onPage=self._draw_body_bg)
        back = PageTemplate(id="Back", frames=[self._cover_frame()],
                            onPage=self._draw_back_bg)
        self.addPageTemplates([cover, control, body, back])

    # -- background painters ---------------------------------------------------
    def _draw_cover_bg(self, canv, doc):
        s = self.spec
        _uc = uni_colors(s)
        prim = _c(_uc["primary"]); acc = _c(_uc["accent"])
        w, h = PAGE_W, PAGE_H
        # outer double rule frame
        canv.setStrokeColor(prim); canv.setLineWidth(2.4)
        canv.rect(0.32 * inch, 0.32 * inch, w - 0.64 * inch, h - 0.64 * inch)
        canv.setLineWidth(0.7)
        canv.rect(0.46 * inch, 0.46 * inch, w - 0.92 * inch, h - 0.92 * inch)
        # classification top & bottom bands
        self._class_band(canv, doc, top=True)
        self._class_band(canv, doc, top=False)
        # thin accent rules flanking the masthead area
        canv.setStrokeColor(acc); canv.setLineWidth(0.8)
        mid = w / 2
        canv.line(0.62 * inch, 6.62 * inch, mid - 0.75 * inch, 6.62 * inch)
        canv.line(mid + 0.75 * inch, 6.62 * inch, w - 0.62 * inch, 6.62 * inch)
        canv.setFont("Helvetica-Bold", 6.5)
        canv.setFillColor(_c("#777777"))
        canv.drawCentredString(mid, 0.62 * inch, "THIS DOCUMENT HAS BEEN DECLASSIFIED IN PART FOR ACADEMIC REVIEW — REPRODUCTION OF ANNEX MATERIAL IS RESTRICTED")

    def _class_band(self, canv, doc, top=True):
        s = self.spec
        w = PAGE_W
        canv.saveState()
        canv.setFillColor(black)
        if top:
            canv.rect(0, PAGE_H - 0.30 * inch, w, 0.30 * inch, stroke=0, fill=1)
            canv.setFillColor(white)
            canv.setFont("Helvetica-Bold", 8)
            canv.drawString(0.35 * inch, PAGE_H - 0.21 * inch, s["classification"])
            canv.drawRightString(w - 0.35 * inch, PAGE_H - 0.21 * inch,
                                 s.get("code", "ILA-2026-000") + "  •  " + s.get("declass", "DECLASSIFIED IN PART — 2026"))
        else:
            canv.rect(0, 0, w, 0.26 * inch, stroke=0, fill=1)
            canv.setFillColor(white)
            canv.setFont("Helvetica-Bold", 8)
            canv.drawString(0.35 * inch, 0.085 * inch, s["classification"])
            canv.drawRightString(w - 0.35 * inch, 0.085 * inch, "VOLUME " + str(s["volume"]) + " OF 30")
        canv.restoreState()

    def _draw_control_bg(self, canv, doc):
        self._draw_body_bg(canv, doc)

    def _draw_body_bg(self, canv, doc):
        s = self.spec
        _uc = uni_colors(s)
        prim = _c(_uc["primary"]); acc = _c(_uc["accent"])
        w, h = PAGE_W, PAGE_H
        # watermark
        canv.saveState()
        canv.translate(w / 2, h / 2)
        canv.rotate(38)
        canv.setFillColor(Color(0, 0, 0, alpha=0.045))
        canv.setFont("Helvetica-Bold", 34)
        canv.drawCentredString(0, 0, s["classification"].split("//")[0].strip() + "  //  " + s.get("code", ""))
        canv.rotate(0)
        # header
        canv.setStrokeColor(acc); canv.setLineWidth(0.6)
        canv.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
        canv.setStrokeColor(prim); canv.setLineWidth(1.6)
        canv.line(MARGIN, PAGE_H - 0.66 * inch, PAGE_W - MARGIN, PAGE_H - 0.66 * inch)
        # small logo, top-left
        logo = s.get("logo")
        if logo and os.path.exists(logo):
            try:
                ir = ImageReader(logo)
                iw, ih = ir.getSize()
                th = 0.34 * inch
                tw = iw * th / ih
                canv.drawImage(ir, MARGIN, PAGE_H - 0.52 * inch - th, tw, th, mask="auto")
            except Exception:
                pass
        canv.setFillColor(prim)
        canv.setFont("Helvetica-Bold", 7.2)
        canv.drawString(MARGIN + 0.42 * inch, PAGE_H - 0.50 * inch,
                        s["university"].upper() + "  •  OFFICE OF ADVANCED RESEARCH")
        canv.setFillColor(_c("#444444"))
        canv.setFont("Helvetica", 6.8)
        canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.50 * inch, s["classification"])
        # footer
        canv.setStrokeColor(acc); canv.setLineWidth(0.6)
        canv.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
        canv.setFillColor(_c("#555555"))
        canv.setFont("Helvetica", 7.5)
        canv.drawString(MARGIN, 0.46 * inch, s.get("code", ""))
        canv.drawCentredString(w / 2, 0.46 * inch, "Page %d" % doc.page)
        canv.setFont("Helvetica-Bold", 7.5)
        canv.setFillColor(prim)
        canv.drawRightString(PAGE_W - MARGIN, 0.46 * inch, s["short_title"].upper())
        canv.restoreState()

    def _draw_back_bg(self, canv, doc):
        s = self.spec
        _uc = uni_colors(s)
        prim = _c(_uc["primary"]); acc = _c(_uc["accent"])
        w, h = PAGE_W, PAGE_H
        canv.setStrokeColor(prim); canv.setLineWidth(2.4)
        canv.rect(0.32 * inch, 0.32 * inch, w - 0.64 * inch, h - 0.64 * inch)
        canv.setLineWidth(0.7)
        canv.rect(0.46 * inch, 0.46 * inch, w - 0.92 * inch, h - 0.92 * inch)
        self._class_band(canv, doc, top=True)
        self._class_band(canv, doc, top=False)


# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
def uni_colors(spec):
    return UNIVERSITIES.get(spec["university"], {"primary": "#A51C30", "accent": "#C4A265"})


def build_styles(spec):
    _uc = uni_colors(spec)
    prim = _c(_uc["primary"]); acc = _c(_uc["accent"])
    styles = getSampleStyleSheet()
    S = {}

    S["Masthead"] = ParagraphStyle("Masthead", fontName="Helvetica-Bold", fontSize=15,
                                   leading=18, alignment=TA_CENTER, textColor=prim,
                                   spaceAfter=2, tracking=4)
    S["MastSub"] = ParagraphStyle("MastSub", fontName="Helvetica", fontSize=8.5,
                                  leading=11, alignment=TA_CENTER, textColor=_c("#444444"),
                                  spaceAfter=2, tracking=2)
    S["CoverTitle"] = ParagraphStyle("CoverTitle", fontName="Times-Bold", fontSize=26,
                                     leading=31, alignment=TA_CENTER, textColor=_c("#111111"),
                                     spaceAfter=8)
    S["CoverSub"] = ParagraphStyle("CoverSub", fontName="Times-Italic", fontSize=13,
                                   leading=17, alignment=TA_CENTER, textColor=prim,
                                   spaceAfter=10)
    S["CoverMeta"] = ParagraphStyle("CoverMeta", fontName="Helvetica", fontSize=8,
                                    leading=11, alignment=TA_CENTER, textColor=_c("#333333"))
    S["Abstract"] = ParagraphStyle("Abstract", fontName="Times-Italic", fontSize=10.5,
                                   leading=14.5, alignment=TA_JUSTIFY, textColor=_c("#222222"),
                                   spaceAfter=6)
    S["SectionHead"] = ParagraphStyle("SectionHead", fontName="Times-Bold", fontSize=15.5,
                                      leading=19, alignment=TA_LEFT, textColor=prim,
                                      spaceBefore=18, spaceAfter=4)
    S["SubHead"] = ParagraphStyle("SubHead", fontName="Times-BoldItalic", fontSize=11.5,
                                  leading=15, alignment=TA_LEFT, textColor=_c("#222222"),
                                  spaceBefore=10, spaceAfter=4)
    S["Body"] = ParagraphStyle("Body", fontName="Times-Roman", fontSize=10.5, leading=14.8,
                               alignment=TA_JUSTIFY, textColor=_c("#111111"), spaceAfter=7)
    S["Bullet"] = ParagraphStyle("Bullet", fontName="Times-Roman", fontSize=10.5, leading=14.2,
                                 alignment=TA_JUSTIFY, textColor=_c("#111111"), spaceAfter=3.5,
                                 leftIndent=20, bulletIndent=6)
    S["Caption"] = ParagraphStyle("Caption", fontName="Times-Italic", fontSize=9, leading=12,
                                  alignment=TA_CENTER, textColor=_c("#333333"), spaceBefore=3,
                                  spaceAfter=1)
    S["Source"] = ParagraphStyle("Source", fontName="Helvetica", fontSize=7, leading=9,
                                 alignment=TA_CENTER, textColor=_c("#777777"), spaceAfter=10)
    S["InsightTitle"] = ParagraphStyle("InsightTitle", fontName="Helvetica-Bold", fontSize=8.5,
                                       leading=11, alignment=TA_LEFT, textColor=prim,
                                       spaceAfter=3, tracking=1)
    S["Insight"] = ParagraphStyle("Insight", fontName="Times-Italic", fontSize=10, leading=13.6,
                                  alignment=TA_JUSTIFY, textColor=_c("#222222"))
    S["TOCEntry"] = ParagraphStyle("TOCEntry", fontName="Times-Roman", fontSize=10.5, leading=16,
                                   alignment=TA_LEFT, textColor=_c("#111111"))
    S["TOCHead"] = ParagraphStyle("TOCHead", fontName="Times-Bold", fontSize=16, leading=20,
                                  alignment=TA_LEFT, textColor=prim, spaceAfter=10)
    S["Ref"] = ParagraphStyle("Ref", fontName="Times-Roman", fontSize=8.7, leading=11.5,
                              alignment=TA_LEFT, textColor=_c("#222222"), spaceAfter=4,
                              leftIndent=22, firstLineIndent=-22)
    S["Cell"] = ParagraphStyle("Cell", fontName="Times-Roman", fontSize=9, leading=12,
                               alignment=TA_LEFT, textColor=_c("#111111"))
    S["CellHead"] = ParagraphStyle("CellHead", fontName="Helvetica-Bold", fontSize=8,
                                   leading=10.5, alignment=TA_LEFT, textColor=white)
    S["Small"] = ParagraphStyle("Small", fontName="Times-Roman", fontSize=9.5, leading=13,
                                alignment=TA_JUSTIFY, textColor=_c("#333333"), spaceAfter=5)
    S["CenterItalic"] = ParagraphStyle("CenterItalic", fontName="Times-Italic", fontSize=10,
                                       leading=14, alignment=TA_CENTER, textColor=_c("#333333"),
                                       spaceAfter=6)
    return styles, S


# ----------------------------------------------------------------------------
# Flowable helpers
# ----------------------------------------------------------------------------
class Ornament(HRFlowable):
    """A classic centre-ornament rule:  —◆— """


def hrule(width=W, color="#C4A265", thickness=0.8, space=6, dash=None):
    col = _c(color) if isinstance(color, str) else color
    return HRFlowable(width=width, thickness=thickness, color=col,
                      spaceBefore=space, spaceAfter=space, dash=dash)


def insight_box(text, styles, prim, acc, label="KEY INSIGHT"):
    inner = [
        Paragraph(label, styles["InsightTitle"]),
        Paragraph(text, styles["Insight"]),
    ]
    t = Table([[inner]], colWidths=[W - 26])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, acc),
        ("BACKGROUND", (0, 0), (-1, -1), _c("#F7F4EC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LINEBEFORE", (0, 0), (0, -1), 3, prim),
    ]))
    return t


def figure_block(spec, fig, styles, max_w=5.6 * inch):
    """fig: dict(img, caption, source, width_ratio)"""
    path = fig["img"]
    if not os.path.exists(path):
        return [Spacer(1, 4)]
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    ratio = fig.get("ratio", 1.0)
    avail = W * 0.80 * ratio
    aspect = iw / ih
    if aspect > 1.2:      # landscape
        tw = min(avail, 4.6 * inch * ratio)
    elif aspect < 0.8:    # portrait
        tw = min(avail, 2.7 * inch * ratio)
    else:                 # square-ish
        tw = min(avail, 3.5 * inch * ratio)
    th = tw * ih / iw
    img = Image(path, width=tw, height=th)
    img.hAlign = "CENTER"
    els = [Spacer(1, 6), img]
    if fig.get("caption"):
        els.append(Paragraph("Figure %s. %s" % (fig.get("num", ""), fig["caption"]), styles["Caption"]))
    if fig.get("source"):
        els.append(Paragraph("Source: %s" % fig["source"], styles["Source"]))
    return [KeepTogether(els)]


def data_table(headers, rows, col_widths, styles, prim, header_bg=None, fontsize=9):
    hdr = [Paragraph(h, styles["CellHead"]) for h in headers]
    body = [[Paragraph(str(c), styles["Cell"]) for c in r] for r in rows]
    data = [hdr] + body
    bg = _c(header_bg) if isinstance(header_bg, str) else (header_bg if header_bg is not None else prim)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), bg),
        ("GRID", (0, 0), (-1, -1), 0.4, _c("#BBBBBB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, _c("#F4F1E8")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


# ----------------------------------------------------------------------------
# Story assembly
# ----------------------------------------------------------------------------
def build_story(spec):
    _, S = build_styles(spec)
    _uc = uni_colors(spec)
    prim = _c(_uc["primary"]); acc = _c(_uc["accent"])
    els = []
    uni = spec["university"]

    # ============================= COVER =============================
    els.append(NextPageTemplate("Control"))
    els.append(Paragraph(uni.upper(), S["Masthead"]))
    els.append(Paragraph("OFFICE OF ADVANCED RESEARCH AND STRATEGIC INTELLIGENCE", S["MastSub"]))
    els.append(Paragraph("ADVANCED RESEARCH MONOGRAPH SERIES  •  VOLUME %d OF 30" % spec["volume"], S["MastSub"]))
    els.append(Spacer(1, 14))
    # logo row: university + partner institutions
    logo_path = spec.get("logo")
    if logo_path and os.path.exists(logo_path):
        ir = ImageReader(logo_path)
        iw, ih = ir.getSize()
        th = 1.05 * inch
        tw = iw * th / ih
        img = Image(logo_path, width=tw, height=th)
        img.hAlign = "CENTER"
        els.append(img)
    partner_logos = spec.get("partner_logos", [])
    if partner_logos:
        els.append(Spacer(1, 6))
        row = []
        for p in partner_logos:
            if os.path.exists(p):
                pir = ImageReader(p)
                piw, pih = pir.getSize()
                pth = 0.42 * inch
                ptw = piw * pth / pih
                row.append(Image(p, width=ptw, height=pth))
        if row:
            pt = Table([row], colWidths=[W / len(row)] * len(row))
            pt.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            els.append(pt)
    els.append(Spacer(1, 16))
    els.append(hrule(width=2.6 * inch, color=acc, thickness=0.8))
    els.append(Spacer(1, 10))
    els.append(Paragraph(spec["title"], S["CoverTitle"]))
    els.append(Paragraph(spec["subtitle"], S["CoverSub"]))
    els.append(Spacer(1, 8))
    els.append(Paragraph("Prepared by %s" % spec.get("author", uni), S["CoverMeta"]))
    els.append(Paragraph("Document Control Number: %s   •   Issued: %s" % (spec["code"], spec["date"]), S["CoverMeta"]))
    els.append(Paragraph("Subject Classification: %s" % spec.get("subject", "Artificial Intelligence"), S["CoverMeta"]))
    els.append(Spacer(1, 12))
    # document control table
    ctrl_rows = [
        ["DOCUMENT ID", spec["code"]],
        ["SERIES", "Advanced Research Monograph Series — Volume %d" % spec["volume"]],
        ["CLASSIFICATION", spec["classification"]],
        ["HANDLING", spec.get("handling", "EYES ONLY — FACULTY AND FELLOWS")],
        ["ORIGINATOR", spec.get("author", "Office of Advanced Research")],
        ["DATE OF ISSUE", spec["date"]],
        ["SUBJECT AREA", spec.get("subject_area", "Artificial Intelligence / Machine Learning")],
        ["DEVELOPMENT STATUS", spec.get("status", "CURRENT — DECLASSIFIED IN PART")],
    ]
    ct = Table([[Paragraph(a, S["CellHead"]), Paragraph(b, S["Cell"])] for a, b in ctrl_rows],
               colWidths=[1.55 * inch, W - 1.55 * inch])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), prim),
        ("GRID", (0, 0), (-1, -1), 0.4, _c("#BBBBBB")),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [white, _c("#F4F1E8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    els.append(ct)
    els.append(Spacer(1, 12))
    els.append(Paragraph("ABSTRACT", S["InsightTitle"]))
    els.append(Paragraph(spec["abstract"], S["Abstract"]))
    els.append(Spacer(1, 8))
    els.append(hrule(width=2.6 * inch, color=acc, thickness=0.8))
    els.append(Spacer(1, 6))
    els.append(Paragraph("Distribution: Restricted Academic • Faculty Review Board • Archive Copy", S["CoverMeta"]))
    els.append(PageBreak())

    # ============================= CONTROL + TOC =============================
    els.append(Paragraph("DOCUMENT CONTROL AND TABLE OF CONTENTS", S["TOCHead"]))
    rev_rows = [
        ["REV", "DATE", "DESCRIPTION", "APPROVED BY"],
        ["0.1", spec["date"], "Initial drafting — source validation", "Senior Editor"],
        ["0.2", spec["date"], "Classification review — annex added", "Review Board"],
        ["1.0", spec["date"], "Release for academic distribution", "Chair, Advanced Research"],
    ]
    rt = data_table(["REV", "DATE", "DESCRIPTION", "APPROVED BY"],
                    rev_rows[1:], [0.5 * inch, 1.0 * inch, W - 2.6 * inch, 1.4 * inch],
                    S, prim)
    rt.hAlign = "CENTER"
    els.append(rt)
    els.append(Spacer(1, 18))
    els.append(Paragraph("TABLE OF CONTENTS", S["TOCHead"]))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC1", fontName="Times-Bold", fontSize=11, leading=17,
                       leftIndent=6, firstLineIndent=-6, textColor=_c("#111111")),
        ParagraphStyle("TOC2", fontName="Times-Roman", fontSize=10, leading=15,
                       leftIndent=30, textColor=_c("#333333")),
    ]
    toc.dotsMinLevel = 0
    els.append(toc)
    els.append(Spacer(1, 14))
    els.append(Paragraph("LIST OF FIGURES", S["TOCHead"]))
    for f in spec.get("figures", []):
        els.append(Paragraph("Figure %s. %s" % (f["num"], f["title"]), S["Small"]))
    els.append(Spacer(1, 10))
    els.append(Paragraph("LIST OF ANNEXES", S["TOCHead"]))
    for a in spec.get("annexes", []):
        els.append(Paragraph("Annex %s. %s" % (a["id"], a["title"]), S["Small"]))
    els.append(PageBreak())

    # ============================= BODY =============================
    els.append(NextPageTemplate("Body"))
    for sec in spec["sections"]:
        # heading registered for TOC
        els.append(Paragraph(sec["title"], S["SectionHead"]))
        # TOC entries are registered via IvyMonograph.afterFlowable
        els.append(hrule(width=W, color=prim, thickness=1.0, space=2))
        for para in sec.get("paras", []):
            els.append(Paragraph(para, S["Body"]))
        for b in sec.get("bullets", []):
            els.append(Paragraph(b, S["Bullet"], bulletText="\u2013"))
        if sec.get("insight"):
            els.append(insight_box(sec["insight"], S, prim, acc))
            els.append(Spacer(1, 6))
        for fig in sec.get("figures", []):
            els.extend(figure_block(spec, fig, S))
    # end matter heading (references flow naturally after the body;
    # if the final figure floated to its own page, references begin beneath it)
    els.append(Paragraph("REFERENCES AND SOURCE MATERIAL", S["TOCHead"]))
    # (TOC entry registered in afterFlowable)
    els.append(Paragraph(
        "<i>Compiler's note:</i> entries marked \u201cpress reporting\u201d or \u201cunverified\u201d reflect "
        "journalistic accounts of non-public programs; they are reproduced for academic "
        "analysis and are not confirmations of program status.", S["Small"]))
    els.append(Spacer(1, 4))
    for i, r in enumerate(spec.get("references", []), 1):
        els.append(Paragraph("[%d]&nbsp; %s" % (i, r), S["Ref"]))
    els.append(PageBreak())

    # ============================= GLOSSARY =============================
    els.append(Paragraph("APPENDIX A — TECHNICAL GLOSSARY", S["TOCHead"]))
    # (TOC entry registered in afterFlowable)
    g_rows = [[Paragraph(t, S["Cell"]), Paragraph(d, S["Cell"])] for t, d in spec.get("glossary", [])]
    gt = Table(g_rows, colWidths=[1.7 * inch, W - 1.7 * inch], repeatRows=0)
    gt.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, _c("#BBBBBB")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, _c("#F4F1E8")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    els.append(gt)
    els.append(PageBreak())

    # ============================= TIMELINE =============================
    els.append(Paragraph("APPENDIX B — CLASSIFIED TIMELINE", S["TOCHead"]))
    # (TOC entry registered in afterFlowable)
    t_rows = [[Paragraph(d, S["Cell"]), Paragraph(e, S["Cell"])] for d, e in spec.get("timeline", [])]
    tt = Table(t_rows, colWidths=[1.15 * inch, W - 1.15 * inch], repeatRows=0)
    tt.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, _c("#BBBBBB")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, _c("#F4F1E8")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    els.append(tt)
    els.append(Spacer(1, 10))
    els.append(insight_box(spec.get("closing_insight", ""), S, prim, acc, label="CLOSING ASSESSMENT"))
    els.append(PageBreak())

    # ============================= BACK COVER =============================
    els.append(NextPageTemplate("Back"))
    els.append(Spacer(1, 0.6 * inch))
    els.append(Paragraph(uni.upper(), S["Masthead"]))
    els.append(Paragraph("OFFICE OF ADVANCED RESEARCH AND STRATEGIC INTELLIGENCE", S["MastSub"]))
    els.append(Spacer(1, 18))
    els.append(Paragraph(spec["title"], S["CoverSub"]))
    els.append(Spacer(1, 10))
    els.append(hrule(width=2.6 * inch, color=acc, thickness=0.8))
    els.append(Spacer(1, 12))
    dist = [
        ("DISTRIBUTION", "Restricted Academic — Faculty Review Board; Departmental Archive; Fellows' Library"),
        ("REPRODUCTION", "Annexes may not be reproduced or translated without written authorization."),
        ("CONTACT", "Office of Advanced Research and Strategic Intelligence, %s" % uni),
        ("NEXT VOLUME", spec.get("next_volume", "See series index")),
    ]
    for k, v in dist:
        els.append(Paragraph("<b>%s.</b> %s" % (k, v), S["Small"]))
    els.append(Spacer(1, 14))
    els.append(Paragraph("— END OF DOCUMENT —", S["CenterItalic"]))
    els.append(Spacer(1, 10))
    els.append(Paragraph(
        "This monograph is one of a thirty-volume series prepared for advanced study in artificial "
        "intelligence. Facts, figures, and attributions were compiled from primary technical literature, "
        "official institutional communications, and documented press reporting; speculative material is "
        "explicitly labelled. The institutional seals reproduced herein are the property of their "
        "respective institutions and are shown for identification purposes only.", S["Small"]))
    return els, toc


def build_pdf(spec, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, spec["filename"])
    doc = IvyMonograph(filename, spec)
    story, _ = build_story(spec)
    doc.multiBuild(story)
    return filename


# small helper for dates
def today():
    return datetime.now(timezone.utc).strftime("%d %B %Y")

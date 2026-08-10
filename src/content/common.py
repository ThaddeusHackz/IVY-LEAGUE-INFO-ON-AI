#!/usr/bin/env python3
"""Shared helpers for the 30-volume content modules."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(ROOT, "assets")
LOGOS = os.path.join(ASSETS, "logos")
PHOTOS = os.path.join(ASSETS, "photos")

DATE = "10 August 2026"
SERIES = "Advanced Research Monograph Series"


def L(name):
    return os.path.join(LOGOS, name)


def P(name):
    return os.path.join(PHOTOS, name)


_CLASS = [
    "TOP SECRET // SPECIAL ACCESS REQUIRED",
    "SECRET // NOFORN",
    "TOP SECRET // ORCON",
    "CONFIDENTIAL // LIMITED DISTRIBUTION",
    "SECRET // EYES ONLY",
    "TOP SECRET // SCI",
]

_HANDLING = [
    "EYES ONLY — FACULTY AND FELLOWS",
    "RESTRICTED ACADEMIC DISTRIBUTION",
    "NOFORN — US/UK ACADEMIC EXCHANGE ONLY",
    "LIMITED DISTRIBUTION — REVIEW BOARD",
]


def V(volume, fname, title, subtitle, university, logo, partners, subject_area,
      abstract, sections, references, glossary, timeline, closing, short_title=None,
      status="CURRENT — DECLASSIFIED IN PART", next_volume=None, keywords="", figures=None,
      annexes=None, author=None):
    """Assemble a full volume spec dict."""
    if short_title is None:
        short_title = title
    if len(short_title) > 52:
        short_title = short_title[:49] + "..."
    if author is None:
        author = "Office of Advanced Research and Strategic Intelligence"
    code = "ILA-2026-%03d" % volume
    classification = _CLASS[(volume - 1) % len(_CLASS)]
    handling = _HANDLING[(volume - 1) % len(_HANDLING)]
    if figures is None:
        figures = []
        for sec in sections:
            for fig in sec.get("figures", []):
                figures.append({"num": fig.get("num", ""), "title": fig.get("caption", "").split(".")[0]})
    if annexes is None:
        annexes = [{"id": "A", "title": "Compartmented Technical Detail (see Section %d)" % len(sections)}]
    return {
        "filename": fname,
        "volume": volume,
        "code": code,
        "title": title,
        "short_title": short_title,
        "subtitle": subtitle,
        "university": university,
        "logo": logo,
        "partner_logos": partners,
        "classification": classification,
        "handling": handling,
        "date": DATE,
        "subject_area": subject_area,
        "status": status,
        "abstract": abstract,
        "author": author,
        "sections": sections,
        "references": references,
        "glossary": glossary,
        "timeline": timeline,
        "closing_insight": closing,
        "figures": figures,
        "annexes": annexes,
        "next_volume": next_volume,
        "keywords": keywords,
        "subject": subject_area,
    }


def sec(title, paras=None, bullets=None, insight=None, figures=None):
    """Section dict shorthand."""
    return {
        "title": title,
        "paras": paras or [],
        "bullets": bullets or [],
        "insight": insight,
        "figures": figures or [],
    }

#!/usr/bin/env python3
"""
build_all.py — Builds all 30 volumes of the Advanced Research Monograph Series.

Usage:  python3 src/build_all.py [volume_number ...]
        (with no arguments, builds all 30 volumes)
"""
import os
import sys
import importlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "src", "content"))

from pdf_framework import build_pdf  # noqa: E402

CONTENT_MODULES = ["content_1", "content_2", "content_3", "content_4", "content_5", "content_6"]
PDF_DIR = os.path.join(ROOT, "pdfs")


def load_volumes():
    vols = []
    for mod in CONTENT_MODULES:
        m = importlib.import_module(mod)
        vols.extend(m.VOLUMES)
    return vols


def main():
    args = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    volumes = load_volumes()
    if args:
        volumes = [v for v in volumes if v["volume"] in args]
    print(f"Building {len(volumes)} volumes into {PDF_DIR} ...")
    for v in volumes:
        fn = build_pdf(v, PDF_DIR)
        print(f"  [Vol {v['volume']:02d}] {os.path.basename(fn)}  ({v['title']})")
    print("Done.")


if __name__ == "__main__":
    main()

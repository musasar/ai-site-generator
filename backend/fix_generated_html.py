"""Utility: fix existing generated index.html files by ensuring charset/viewport in <head>.

Run from project root:
    python backend/fix_generated_html.py
"""
import glob
import os
from site_generator import _ensure_meta_in_head


def main():
    base = os.path.join("backend", "generated_sites")
    pattern = os.path.join(base, "*", "index.html")
    files = glob.glob(pattern)
    if not files:
        print("No generated index.html files found.")
        return
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            fixed = _ensure_meta_in_head(html)
            if fixed != html:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(fixed)
                print(f"Fixed: {path}")
            else:
                print(f"OK: {path}")
        except Exception as e:
            print(f"Error processing {path}: {e}")


if __name__ == '__main__':
    main()

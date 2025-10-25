"""Utility: fix existing generated index.html files by ensuring charset/viewport in <head>.

Run from project root:
    python backend/fix_generated_html.py
"""
import glob
import os
from backend.site_generator import _ensure_meta_in_head


def find_generated_index_files(root_dir: str):
    """Find index.html files under any generated_sites directory inside root_dir."""
    pattern = os.path.join(root_dir, "**", "generated_sites", "**", "index.html")
    return glob.glob(pattern, recursive=True)


def main():
    root = os.getcwd()
    files = find_generated_index_files(root)
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

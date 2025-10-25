import os
import subprocess
from datetime import datetime
import re
import os

def ollama(prompt):
    """Ollama CLI ile modelden çıktı alır."""
    result = subprocess.run(
        ["ollama", "run", "codellama:7b-code", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def generate_site(prompt_text):
    """Kullanıcı prompt'una göre site üretir."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    site_name = f"site_{timestamp}"
    folder = os.path.join("backend", "generated_sites", site_name)
    os.makedirs(folder, exist_ok=True)

    html_prompt = f"'{prompt_text}' temasına uygun modern bir web sitesi için HTML oluştur. style.css ve index.js dosyalarına bağlantı ekle."
    css_prompt = f"'{prompt_text}' temalı web sitesi için sade bir style.css oluştur. Renk paleti temaya uygun olsun."
    js_prompt = f"'{prompt_text}' web sitesine basit bir interaktif index.js oluştur. Sayfa yüklendiğinde konsola '{prompt_text} yüklendi!' yaz."

    # Allow a mock mode for testing when Ollama is not available
    if os.getenv("AI_SITE_GENERATOR_MOCK", "false").lower() in ("1", "true", "yes"):
        html = f"<!doctype html>\n<html>\n<body>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<h1>{prompt_text}</h1>\n</body>\n</html>"
        css = "body { font-family: Arial, sans-serif; }"
        js = f"console.log('{prompt_text} yüklendi!')"
    else:
        html = ollama(html_prompt)
    css = ollama(css_prompt)
    js = ollama(js_prompt)

    # Ensure meta charset and viewport are in the <head>
    try:
        html = _ensure_meta_in_head(html)
    except Exception:
        # If post-processing fails, keep original HTML
        pass

    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(folder, "style.css"), "w", encoding="utf-8") as f:
        f.write(css)
    with open(os.path.join(folder, "index.js"), "w", encoding="utf-8") as f:
        f.write(js)

    # Daha basit bir response için sadece site adını döndürüyoruz
    return site_name


def _ensure_meta_in_head(html: str) -> str:
    """Ensure charset and viewport meta tags are inside the <head>.

    This is a best-effort, resilient string-based fixer so generated HTML
    from the model displays correctly in browsers and satisfies linters.
    """
    if not isinstance(html, str):
        return html

    metas = []
    # find charset meta
    for m in re.finditer(r"<meta[^>]*charset[^>]*>", html, flags=re.IGNORECASE):
        metas.append(m.group(0))
    # find viewport meta
    for m in re.finditer(r"<meta[^>]*name=[\'\"]viewport[\'\"][^>]*>", html, flags=re.IGNORECASE):
        metas.append(m.group(0))

    if not metas:
        return html

    # remove duplicates and preserve order
    seen = set()
    metas = [m for m in metas if not (m in seen or seen.add(m))]

    # remove found metas from html
    for m in metas:
        html = html.replace(m, "")

    # ensure a <head> exists
    if re.search(r"<head[^>]*>", html, flags=re.IGNORECASE):
        # insert metas right after opening head tag
        html = re.sub(r"(<head[^>]*>)", lambda mo: mo.group(1) + "\n" + "\n".join(metas), html, count=1, flags=re.IGNORECASE)
    else:
        # no head tag: create one before body or before html end
        if re.search(r"<html[^>]*>", html, flags=re.IGNORECASE):
            html = re.sub(r"(<html[^>]*>)", lambda mo: mo.group(1) + "\n<head>\n" + "\n".join(metas) + "\n</head>", html, count=1, flags=re.IGNORECASE)
        else:
            # fallback: prepend head
            html = "<head>\n" + "\n".join(metas) + "\n</head>\n" + html

    return html

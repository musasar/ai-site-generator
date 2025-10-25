import os
import subprocess
from datetime import datetime

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
    folder = f"backend/generated_sites/site_{timestamp}"
    os.makedirs(folder, exist_ok=True)

    html_prompt = f"'{prompt_text}' temasına uygun modern bir web sitesi için HTML oluştur. style.css ve index.js dosyalarına bağlantı ekle."
    css_prompt = f"'{prompt_text}' temalı web sitesi için sade bir style.css oluştur. Renk paleti temaya uygun olsun."
    js_prompt = f"'{prompt_text}' web sitesine basit bir interaktif index.js oluştur. Sayfa yüklendiğinde konsola '{prompt_text} yüklendi!' yaz."

    html = ollama(html_prompt)
    css = ollama(css_prompt)
    js = ollama(js_prompt)

    with open(f"{folder}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    with open(f"{folder}/style.css", "w", encoding="utf-8") as f:
        f.write(css)
    with open(f"{folder}/index.js", "w", encoding="utf-8") as f:
        f.write(js)

    return folder

import os
import subprocess
from datetime import datetime
import re
import os


def check_ollama_installed() -> bool:
    """Return True if the `ollama` CLI appears to be available on PATH."""
    try:
        # Prefer a lightweight version check
        res = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return res.returncode == 0
    except FileNotFoundError:
        return False

def ollama(prompt):
    """Ollama CLI ile modelden çıktı alır."""
    result = subprocess.run(
        ["ollama", "run", "codellama:7b-code", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def generate_site(prompt_text, template: str = "modern"):
    """Kullanıcı prompt'una göre site üretir.

    template: 'modern' | 'classic' | 'creative'
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    site_name = f"site_{timestamp}"
    folder = os.path.join("backend", "generated_sites", site_name)
    os.makedirs(folder, exist_ok=True)

    # Base prompts
    html_prompt = f"'{prompt_text}' temasına uygun bir web sitesi için HTML oluştur. style.css ve index.js dosyalarına bağlantı ekle."
    css_prompt = f"'{prompt_text}' temalı web sitesi için sade bir style.css oluştur. Renk paleti temaya uygun olsun."
    js_prompt = f"'{prompt_text}' web sitesine basit bir interaktif index.js oluştur. Sayfa yüklendiğinde konsola '{prompt_text} yüklendi!' yaz."

    # Allow a mock mode for testing when Ollama is not available
    mock_mode = os.getenv("AI_SITE_GENERATOR_MOCK", "false").lower() in ("1", "true", "yes")
    if mock_mode:
        html, css, js = _get_mock_templates(prompt_text, template)
    else:
        # If Ollama is not installed, provide a clear error rather than failing cryptically
        if not check_ollama_installed():
            raise RuntimeError(
                "Ollama CLI bulunamadı. Geliştirme sırasında mock modu kullanmak için environment variable AI_SITE_GENERATOR_MOCK=true ayarlayabilirsiniz, veya Ollama'yı kurun: https://ollama.com"
            )

        # Add template guidance to prompts when using Ollama
        html_prompt = f"{html_prompt} {_get_template_guidance(template)}"
        css_prompt = f"{css_prompt} {_get_template_guidance(template)}"

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


def _get_mock_templates(prompt_text, template):
    """Return mock HTML, CSS, JS tuple for given template."""
    templates = {
        "modern": {
            "html": """<!DOCTYPE html>
<html lang=\"tr\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>{PROMPT}</title>\n    <link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n    <div class=\"container\">\n        <header class=\"modern-header\">\n            <h1>{PROMPT}</h1>\n            <p>Modern ve minimalist tasarım</p>\n        </header>\n        <main>\n            <section class=\"hero\">\n                <h2>Hoş Geldiniz</h2>\n                <p>Bu {PROMPT} için oluşturulmuş modern bir web sitesidir.</p>\n                <button class=\"cta-button\">Keşfet</button>\n            </section>\n        </main>\n    </div>\n    <script src=\"index.js\"></script>\n</body>\n</html>""",
            "css": """* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}\n\nbody {\n    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\n    line-height: 1.6;\n    color: #333;\n    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n    min-height: 100vh;\n}\n\n.container {\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 0 20px;\n}\n\n.modern-header {\n    text-align: center;\n    padding: 4rem 0 2rem;\n    color: white;\n}\n\n.modern-header h1 {\n    font-size: 3rem;\n    margin-bottom: 1rem;\n    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);\n}\n\n.modern-header p {\n    font-size: 1.2rem;\n    opacity: 0.9;\n}\n\n.hero {\n    background: white;\n    padding: 3rem;\n    border-radius: 15px;\n    box-shadow: 0 10px 30px rgba(0,0,0,0.2);\n    text-align: center;\n    margin: 2rem 0;\n}\n\n.hero h2 {\n    color: #333;\n    margin-bottom: 1rem;\n    font-size: 2rem;\n}\n\n.hero p {\n    color: #666;\n    margin-bottom: 2rem;\n    font-size: 1.1rem;\n}\n\n.cta-button {\n    background: #667eea;\n    color: white;\n    border: none;\n    padding: 12px 30px;\n    font-size: 1.1rem;\n    border-radius: 25px;\n    cursor: pointer;\n    transition: all 0.3s ease;\n}\n\n.cta-button:hover {\n    background: #764ba2;\n    transform: translateY(-2px);\n    box-shadow: 0 5px 15px rgba(0,0,0,0.2);\n}""",
            "js": "console.log('{PROMPT} modern tema ile yüklendi!');\n\ndocument.addEventListener('DOMContentLoaded', function() {\n    const button = document.querySelector('.cta-button');\n    if (button) {\n        button.addEventListener('click', function() {\n            alert('{PROMPT} sitesine hoş geldiniz!');\n        });\n    }\n});"
        },
        "classic": {
            "html": """<!DOCTYPE html>\n<html lang=\"tr\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>{PROMPT}</title>\n    <link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n    <div class=\"classic-container\">\n        <header class=\"classic-header\">\n            <nav class=\"classic-nav\">\n                <div class=\"logo\">{PROMPT}</div>\n                <ul class=\"nav-links\">\n                    <li><a href=\"#home\">Ana Sayfa</a></li>\n                    <li><a href=\"#about\">Hakkımızda</a></li>\n                    <li><a href=\"#contact\">İletişim</a></li>\n                </ul>\n            </nav>\n        </header>\n        \n        <main class=\"classic-main\">\n            <section id=\"home\" class=\"hero-section\">\n                <div class=\"hero-content\">\n                    <h1>{PROMPT}</h1>\n                    <p class=\"subtitle\">Profesyonel ve Klasik Çözümler</p>\n                    <button class=\"classic-btn\">Daha Fazla Bilgi</button>\n                </div>\n            </section>\n        </main>\n    </div>\n    <script src=\"index.js\"></script>\n</body>\n</html>""",
            "css": """* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}\n\nbody {\n    font-family: 'Georgia', 'Times New Roman', serif;\n    line-height: 1.6;\n    color: #333;\n    background-color: #f8f9fa;\n}\n\n.classic-container {\n    max-width: 1200px;\n    margin: 0 auto;\n}\n\n.classic-header {\n    background: #2c3e50;\n    color: white;\n    padding: 1rem 0;\n    box-shadow: 0 2px 5px rgba(0,0,0,0.1);\n}\n\n.classic-nav {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    padding: 0 2rem;\n}\n\n.logo {\n    font-size: 1.8rem;\n    font-weight: bold;\n    color: #ecf0f1;\n}\n\n.nav-links {\n    display: flex;\n    list-style: none;\n    gap: 2rem;\n}\n\n.nav-links a {\n    color: #bdc3c7;\n    text-decoration: none;\n    transition: color 0.3s ease;\n    font-size: 1.1rem;\n}\n\n.nav-links a:hover {\n    color: #ecf0f1;\n}\n\n.classic-main {\n    padding: 2rem;\n}\n\n.hero-section {\n    background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);\n    color: white;\n    padding: 4rem 2rem;\n    text-align: center;\n    border-radius: 8px;\n    margin-top: 2rem;\n}\n\n.hero-content h1 {\n    font-size: 3rem;\n    margin-bottom: 1rem;\n    font-weight: normal;\n}\n\n.subtitle {\n    font-size: 1.3rem;\n    margin-bottom: 2rem;\n    opacity: 0.9;\n    font-style: italic;\n}\n\n.classic-btn {\n    background: #e74c3c;\n    color: white;\n    border: none;\n    padding: 12px 30px;\n    font-size: 1.1rem;\n    border-radius: 4px;\n    cursor: pointer;\n    transition: background 0.3s ease;\n    font-family: inherit;\n}\n\n.classic-btn:hover {\n    background: #c0392b;\n}""",
            "js": "console.log('{PROMPT} classic tema ile yüklendi!');\n\ndocument.addEventListener('DOMContentLoaded', function() {\n    const button = document.querySelector('.classic-btn');\n    if (button) {\n        button.addEventListener('click', function() {\n            alert('{PROMPT} - Klasik ve Profesyonel');\n        });\n    }\n});"
        },
        "creative": {
            "html": """<!DOCTYPE html>\n<html lang=\"tr\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>{PROMPT}</title>\n    <link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n    <div class=\"creative-container\">\n        <header class=\"creative-header\">\n            <h1 class=\"creative-title\">{PROMPT}</h1>\n            <p class=\"creative-subtitle\">Yaratıcı ve Renkli Deneyim</p>\n        </header>\n        \n        <main class=\"creative-main\">\n            <div class=\"color-blocks\">\n                <div class=\"color-block block-1\">\n                    <h3>Yenilikçi</h3>\n                    <p>Modern çözümler</p>\n                </div>\n                <div class=\"color-block block-2\">\n                    <h3>Yaratıcı</h3>\n                    <p>Özgün tasarımlar</p>\n                </div>\n                <div class=\"color-block block-3\">\n                    <h3>Dinamik</h3>\n                    <p>Canlı etkileşimler</p>\n                </div>\n            </div>\n            \n            <button class=\"creative-btn\">Hayal Et!</button>\n        </main>\n    </div>\n    <script src=\"index.js\"></script>\n</body>\n</html>""",
            "css": """* {\n    margin: 0;\n    padding: 0;\n    box-sizing: border-box;\n}\n\nbody {\n    font-family: 'Comic Sans MS', cursive, sans-serif;\n    line-height: 1.6;\n    color: #333;\n    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);\n    background-size: 400% 400%;\n    animation: gradientShift 15s ease infinite;\n    min-height: 100vh;\n}\n\n@keyframes gradientShift {\n    0% { background-position: 0% 50%; }\n    50% { background-position: 100% 50%; }\n    100% { background-position: 0% 50%; }\n}\n\n.creative-container {\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 2rem;\n}\n\n.creative-header {\n    text-align: center;\n    margin-bottom: 3rem;\n    color: white;\n    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);\n}\n\n.creative-title {\n    font-size: 4rem;\n    margin-bottom: 1rem;\n    animation: bounce 2s infinite;\n}\n\n@keyframes bounce {\n    0%, 100% { transform: translateY(0); }\n    50% { transform: translateY(-10px); }\n}\n\n.creative-subtitle {\n    font-size: 1.5rem;\n    opacity: 0.9;\n}\n\n.creative-main {\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    gap: 2rem;\n}\n\n.color-blocks {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n    gap: 1.5rem;\n    width: 100%;\n    max-width: 800px;\n}\n\n.color-block {\n    padding: 2rem;\n    border-radius: 20px;\n    text-align: center;\n    color: white;\n    box-shadow: 0 10px 30px rgba(0,0,0,0.3);\n    transition: transform 0.3s ease;\n}\n\n.color-block:hover {\n    transform: scale(1.05);\n}\n\n.block-1 {\n    background: linear-gradient(135deg, #ff6b6b, #ee5a24);\n}\n\n.block-2 {\n    background: linear-gradient(135deg, #4ecdc4, #00b894);\n}\n\n.block-3 {\n    background: linear-gradient(135deg, #45b7d1, #0984e3);\n}\n\n.color-block h3 {\n    font-size: 1.5rem;\n    margin-bottom: 0.5rem;\n}\n\n.creative-btn {\n    background: linear-gradient(135deg, #a29bfe, #6c5ce7);\n    color: white;\n    border: none;\n    padding: 15px 40px;\n    font-size: 1.3rem;\n    border-radius: 50px;\n    cursor: pointer;\n    transition: all 0.3s ease;\n    box-shadow: 0 5px 15px rgba(0,0,0,0.2);\n    font-family: inherit;\n}\n\n.creative-btn:hover {\n    transform: scale(1.1) rotate(5deg);\n    box-shadow: 0 10px 25px rgba(0,0,0,0.3);\n}""",
                "js": "console.log('{PROMPT} creative tema ile yüklendi!');\n\ndocument.addEventListener('DOMContentLoaded', function() {\n    const button = document.querySelector('.creative-btn');\n    if (button) {\n        button.addEventListener('click', function() {\n            button.textContent = 'Harika! 🎉';\n            setTimeout(() => {\n                button.textContent = 'Hayal Et!';\n            }, 2000);\n        });\n    }\n    \n    // Add floating animation to color blocks\n    const blocks = document.querySelectorAll('.color-block');\n    blocks.forEach((block, index) => {\n        block.style.animation = `float ${3 + index * 0.5}s ease-in-out infinite`;\n    });\n});"
        }
    }
    # return tuple (html, css, js)
    t = templates.get(template, templates["modern"])
    # replace placeholder with actual prompt
    html = t["html"].replace("{PROMPT}", prompt_text)
    css = t["css"].replace("{PROMPT}", prompt_text)
    js = t["js"].replace("{PROMPT}", prompt_text)
    return html, css, js


def _get_template_guidance(template):
    """Return template-specific guidance for Ollama prompts."""
    guidance = {
        "modern": "Modern, minimalist ve temiz bir tasarım kullan. Bol beyaz alan, basit geometrik şekiller ve gradient arkaplanlar kullan.",
        "classic": "Klasik, profesyonel ve geleneksel bir tasarım kullan. Koyu renkler, serif yazı tipleri ve structured layout kullan.",
        "creative": "Yaratıcı, renkli ve dinamik bir tasarım kullan. Canlı renkler, animasyonlar, gradientler ve interactive elementler ekle."
    }
    return guidance.get(template, guidance["modern"])

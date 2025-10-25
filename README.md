# AI Site Generator

Lightweight local website generator that uses an LLM (Ollama CLI or mock mode) to produce a small static site (index.html, style.css, index.js) from a user prompt. This repo contains a FastAPI backend and a React (Vite) frontend to create and preview generated sites.

## Quick summary
- Backend: Python + FastAPI (serves generated sites under `/sites` and provides `/generate` POST endpoint)
- Frontend: React + Vite (UI to submit prompts, choose a theme, and preview generated site in an iframe)
- Generation: Ollama CLI integration (optional). A mock mode is available for development and CI.

## Quickstart (recommended)
These steps start the project locally using the provided helper scripts.

Linux / macOS
```bash
# make the script executable (first time)
chmod +x start-project.sh
./start-project.sh
```

Windows (PowerShell)
```powershell
# If you hit execution policy blocks, run once with elevated privileges:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start-project.ps1
```

Manual (if you prefer)
```bash
# backend (create/activate your venv first)
python -m venv .venv; source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py

# frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open the frontend URL (Vite will output the address, typically http://localhost:5173). The backend is available at http://localhost:8000 and API docs at http://localhost:8000/docs.

## Mock mode (recommended for local dev without Ollama)
Set the environment variable to force mock templates instead of calling Ollama:

PowerShell
```powershell
$env:AI_SITE_GENERATOR_MOCK = 'true'
```

Linux / macOS
```bash
export AI_SITE_GENERATOR_MOCK=true
```

When mock mode is enabled the backend returns one of three built-in templates (modern / classic / creative) and does not call Ollama.

## Tests
There is a small pytest integration test that validates `generate_site` in mock mode.

```bash
# from repo root
pip install -r requirements.txt
pytest -q
```

CI: A minimal GitHub Actions workflow is present at `.github/workflows/ci.yml` which runs the tests on push/PR and sets `AI_SITE_GENERATOR_MOCK=true` in the job.

## Scripts
- `start-project.sh` — Bash helper that checks Python/Node, enables mock mode if Ollama not present, creates a venv, installs Python deps and starts backend + frontend.
- `start-project.ps1` — PowerShell helper for Windows with similar behavior.
- `backend/fix_generated_html.py` — Utility that scans any `generated_sites/**/index.html` and ensures meta charset/viewport tags are placed in `<head>`.

## Generated output
Generated sites are written into `backend/generated_sites/<site_name>/`. These are ephemeral development artifacts and are ignored by git via `.gitignore`.

To remove generated outputs:

PowerShell
```powershell
Remove-Item -Recurse -Force .\backend\generated_sites\* -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\backend\backend\generated_sites\* -ErrorAction SilentlyContinue
```

Linux / macOS
```bash
rm -rf backend/generated_sites/* backend/backend/generated_sites/*
```

## Development notes
- If you run without mock mode the backend will check for `ollama` on PATH and return a friendly error if it is not installed.
- The `/generate` endpoint validates the prompt and returns HTTP 400 for empty prompts and HTTP 500 with helpful details for generation errors.
- The frontend posts form data (`prompt` and `template`) to `/generate` and previews the returned static site URL in an iframe.

## Contributing
- Run tests before opening a PR
- Keep generated files out of commits (they're ignored by `.gitignore`)

## License
MIT
Harika 💥 — çok net bir vizyon bu.

Senin hedefin şu şekilde özetlenebilir:
💡 “Kullanıcı prompt girsin → yapay zeka otomatik olarak web sitesini oluştursun → ben de bunu bir hizmet (SaaS gibi) olarak sunayım.”
Bu AI Site Generator fikri, hem teknik hem ticari olarak yapılabilir bir iş — hatta 2025’te en hızlı büyüyen nişlerden biri.

Şimdi adım adım sana teknik yol haritası + gelir modeli planını vereyim 👇
🧠 1. Ürünün Temeli: “AI Web Site Generator”
Senin sistemin şu şekilde çalışacak:

Kullanıcı prompt yazar → “bir diyetisyen sitesi istiyorum”
↓
AI (Ollama veya API tabanlı model) HTML/CSS/JS üretir
↓
Sistem bu dosyaları bir klasörde oluşturur
↓
Kullanıcıya önizleme ve indirme linki verir
Bunu iki şekilde hayata geçirebilirsin:
⚙️ 2. Teknik Seçenekler
🔹 A. Lokal Model (Ollama)
Avantajlar:

Ücretsiz çalışır (API ücreti yok)
Veriler senin bilgisayarda kalır
Dezavantajlar:

Hosting zor (her kullanıcı için model çalışmaz)
Sunucu gücü gerekebilir
⚙️ En uygun: MVP (ilk sürüm, test) aşamasında — kendi bilgisayarında veya küçük sunucuda.
🔹 B. API Tabanlı (OpenAI, Anthropic, Mistral vb.)
Avantajlar:

Kullanıcı sayısı artsa bile kolay ölçeklenir
Kod sade (model bulundurmazsın)
Dezavantajlar:

Token başına ücret ödersin
Veriler dış servise gider
⚙️ En uygun: Ürün tutarsa, profesyonel SaaS sürümüne geçerken.
🧩 3. Teknoloji Yığını (Stack Önerisi)
AlanÖneriBackendPython (FastAPI) veya Node.js (Express)FrontendReact + TailwindAI BağlantısıOllama CLI / API veya OpenAI APIDepolamaSQLite (başlangıçta), sonrasında PostgreSQLHostingRender / Railway / Vercel (Frontend) + Ollama LocalÖdemeStripe / PayTR / IyzicoKimlikGitHub OAuth veya e-posta şifre💸 4. Gelir Modeli Fikirleri
ModelAçıklamaFreemium3 ücretsiz site, sonrası ücretliKredi SistemiHer prompt 1 kredi — kullanıcı kredi satın alırAbonelik (SaaS)Aylık 199 TL / sınırsız siteKurumsal Paket“Diyetisyenler için hazır site şablonları” gibi niş paketler🔥 Türkiye’de PayTR veya Iyzico entegrasyonu çok mantıklı olur. (Zaten daha önce Bagisto ile düşündüğün gibi.)
🧰 5. Geliştirme Aşamaları
AşamaHedefTeknoloji1. MVP (yerel)Prompt → HTML/CSS/JS klasörü oluşturPython + Ollama2. Web ArayüzüKullanıcıdan prompt al → web üzerinden site oluşturFastAPI + React3. Önizleme & KaydetmeOluşturulan siteyi canlı gösterIframe veya static serve4. Kullanıcı YönetimiGiriş, kayıt, site geçmişiJWT Auth5. Ödeme & Kredi SistemiPayTR / Stripe entegrasyonuREST API6. Yayın & PazarlamaDemo sayfası, sosyal medya, GitHubSEO + demo repo🧠 6. Spec-Kit ile Entegrasyon Fikri
Spec-Kit burada “AI workflow” kısmını düzenli hale getirebilir:

Prompt → Spec oluştur
Spec → Plan oluştur
Plan → Implement (HTML/CSS/JS üretimi)
Yani kullanıcı prompt’u verir → Spec-Kit “plan” dosyası hazırlar → senin sistemin o plana göre kod üretir.

Bu sayede yapay zekanın çıktıları daha tutarlı olur.
💬 7. Örnek prompt iş akışı
Kullanıcı yazıyor:

“Yoga eğitmeni için tek sayfalık modern web sitesi”
AI üretiyor:

index.html
style.css
index.js
Senin sistem:

projeler/yoga_egitmeni_20251025 klasörünü oluşturur
Dosyaları kaydeder
Kullanıcıya tarayıcıda gösterir (örnek: https://mysitegen.app/yoga_egitmeni_20251025/)
🔥 8. Satılabilirlik Önerileri
NişAçıklama💼 Portföy SiteleriFreelancer’lara, CV sahiplerine🍽️ Kafe & RestoranMenü tanıtım siteleri🧘‍♀️ Diyetisyen & YogaHizmet tanıtım siteleri🎨 TasarımcılarŞablon tabanlı mini portföyler🛍️ Ürün Landing PagesReklam kampanyaları için✳️ 9. İleri Aşama: Hosting + Alan Adı Otomasyonu
Büyüdüğünde şunu da ekleyebilirsin:

Kullanıcı “yayınla” dediğinde otomatik olarak Netlify veya Vercel’e deploy etsin.
Kullanıcıya kullanicisite.aiwebs.app gibi alt alan adı ver.
İstersen ben sana ilk sürümün (MVP) için dosya yapısı + çalışan kod iskeletini hazırlayayım:

/backend/app.py → FastAPI API
/frontend → basit React formu
/generator/site_generator.py → Ollama ile site oluşturucu
Ve her şey lokal çalışacak (henüz hosting yok).

## Setup & Run (Quick)

Ön koşullar:
- Python 3.11+ (veya 3.10)
- Node.js ve npm
- (Opsiyonel) Ollama CLI yüklü ve PATH'e ekli — eğer yoksa mock mod ile test edebilirsiniz.

Backend kurulum ve çalıştırma:

1. Sanal ortam oluşturup aktive edin (opsiyonel ama önerilir):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Eğer Ollama kurulu değilse ve yine de akışı test etmek istiyorsanız, mock modunu etkinleştirin:

```powershell
setx AI_SITE_GENERATOR_MOCK true
# veya sadece oturum için: $env:AI_SITE_GENERATOR_MOCK = 'true'
```

3. Backend'i çalıştırın:

```powershell
# Project root'ta çalıştırın
python .\backend\app.py
# veya
# python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Frontend kurulum ve çalıştırma:

```powershell
cd frontend
npm install
npm run dev
```

Ardından tarayıcıda Vite'in verdiği localhost adresine gidin (ör. http://localhost:5173). Prompt girip "Site Oluştur" butonuna bastığınızda backend modeli çağıracak, üretim klasörünü `backend/generated_sites/site_<timestamp>` içinde oluşturacak ve önizlemeyi iframe içinde `http://localhost:8000/sites/<site_name>/index.html` ile gösterecektir.


## Running tests

There is a small integration test suite that verifies `generate_site` in mock mode. To run the tests locally:

```powershell
# from project root
pip install -r requirements.txt
pytest -q
```

The tests will create and remove temporary folders under `backend/generated_sites` and run quickly in mock mode.
## Cleaning up generated sites
The `generated_sites` folders contain the output created by the app and can be safely removed when you want to free disk space.
To remove all generated sites created during development run (PowerShell):
```powershell
# remove primary generated_sites (used by app mounting)
Remove-Item -Recurse -Force .\backend\generated_sites\* -ErrorAction SilentlyContinue
# also remove any nested generated sites (some runs created backend/backend/generated_sites)
Remove-Item -Recurse -Force .\backend\backend\generated_sites\* -ErrorAction SilentlyContinue
```
To avoid committing generated output to git, a `.gitignore` entry was added for these folders.

## 🚀 Hızlı Başlangıç (script'lerle)

Projeyi tek komutla başlatmak için iki yardımcı script ekledim:

- `start-project.sh` — Linux / macOS için (bash)
- `start-project.ps1` — Windows PowerShell için

Kullanım:

Linux / macOS:
```bash
chmod +x start-project.sh
./start-project.sh
```

Windows (PowerShell):
```powershell
.\start-project.ps1
```

Script'ler şu işleri yapar:
- Python ve Node.js kontrolleri
- Ollama yoksa mock modu etkinleştirme
- Sanal ortam oluşturma ve bağımlılık yükleme (backend)
- Backend ve frontend servislerini başlatma

Alternatif (manuel) başlatma:
```bash
# Backend
python backend/app.py

# Frontend (yeni terminal)
cd frontend && npm install && npm run dev
```

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.site_generator import generate_site
from backend.premium_templates import guidance_for, get_template_info
import uvicorn
import os
import asyncio

app = FastAPI()

# CORS (Frontend erişimi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik olarak oluşturulan siteleri /sites altında sun
# Support both expected path and nested path (some runs created backend/backend/generated_sites)
candidates = [os.path.join("backend", "generated_sites"), os.path.join("backend", "backend", "generated_sites")]
sites_dir = None
for c in candidates:
    if os.path.exists(c):
        sites_dir = c
        break
# default to the primary path if none exist yet
if not sites_dir:
    sites_dir = candidates[0]
os.makedirs(sites_dir, exist_ok=True)
app.mount("/sites", StaticFiles(directory=sites_dir), name="sites")

@app.post("/generate")
async def generate(prompt: str = Form(...), template: str = Form("modern")):
    """Kullanıcı prompt'una göre web sitesi üretir (bloklayıcı iş parçacığında çalıştırılır)."""
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt boş olamaz. Lütfen bir açıklama girin.")

    try:
        # generate_site çalışması bloklayıcı olabilir (subprocess). Threadpool'da çalıştırıyoruz.
        site_name = await asyncio.to_thread(generate_site, prompt, template)
        url = f"http://localhost:8000/sites/{site_name}/index.html"
        return {"status": "ok", "site": site_name, "url": url}
    except Exception as e:
        # Return structured JSON error so frontend can display friendly messages
        raise HTTPException(status_code=500, detail=f"Site oluşturma hatası: {str(e)}")


@app.post("/api/generate")
async def api_generate(prompt: str = Form(...), template_type: str = Form("minimalist"), template: str = Form("modern")):
    """API endpoint for generation that supports premium `template_type`.

    - `template_type` is a premium template key (e.g. minimalist, kurumsal, creative).
    - Falls back to `template` if mapping is not found.
    """
    if not prompt or not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt boş olamaz. Lütfen bir açıklama girin.")

    # Enrich prompt with premium guidance if present
    guidance = guidance_for(template_type) or ""
    enriched_prompt = f"{guidance}\nKullanıcı isteği: {prompt}" if guidance else prompt

    # Determine which base template to use (map premium keys to mock templates)
    info = get_template_info(template_type)
    mapped_template = info.get("map_to") if info else template

    try:
        site_name = await asyncio.to_thread(generate_site, enriched_prompt, mapped_template)
        url = f"http://localhost:8000/sites/{site_name}/index.html"
        return {"status": "ok", "site": site_name, "url": url, "template_type": template_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Site oluşturma hatası: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

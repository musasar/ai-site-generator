from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from site_generator import generate_site
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
sites_dir = os.path.join("backend", "generated_sites")
os.makedirs(sites_dir, exist_ok=True)
app.mount("/sites", StaticFiles(directory=sites_dir), name="sites")

@app.post("/generate")
async def generate(prompt: str = Form(...)):
    """Kullanıcı prompt'una göre web sitesi üretir (bloklayıcı iş parçacığında çalıştırılır)."""
    # generate_site çalışması bloklayıcı olabilir (subprocess). Threadpool'da çalıştırıyoruz.
    site_name = await asyncio.to_thread(generate_site, prompt)
    url = f"http://localhost:8000/sites/{site_name}/index.html"
    return {"status": "ok", "site": site_name, "url": url}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

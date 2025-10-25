from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from site_generator import generate_site
import uvicorn

app = FastAPI()

# CORS (Frontend erişimi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(prompt: str = Form(...)):
    """Kullanıcı prompt'una göre web sitesi üretir."""
    path = generate_site(prompt)
    return {"status": "ok", "path": path}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

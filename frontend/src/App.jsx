import React, { useState, useRef } from "react";
import axios from "axios";
import Preview from "./components/Preview";
import "./App.css";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState("modern");
  const [selectedPremium, setSelectedPremium] = useState("minimalist");
  const textareaRef = useRef(null);

  const examples = [
    "Tek sayfalık modern portföy sitesi - fotoğrafçı",
    "Kahve dükkanı için sıcak ve samimi tanıtım sitesi",
    "Diyetisyen için profesyonel tek sayfa açıklama sitesi"
  ];

  const handleGenerate = async () => {
    setError("");
    setSuccessMsg("");
    setLoading(true);
    const formData = new FormData();
    formData.append("prompt", prompt);
    // send premium template_type for the new API; include legacy 'template' for fallback
    formData.append("template_type", selectedPremium);
    formData.append("template", selectedTemplate);

    try {
      const res = await axios.post("http://localhost:8000/api/generate", formData);
      setUrl(res.data.url);
    } catch (err) {
      console.error(err);
      const msg = err?.response?.data?.detail || err.message || "Bilinmeyen hata";
      setError(`Oluşturma sırasında hata: ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  const handleUseExample = (ex) => {
    setPrompt(ex);
    // focus textarea after picking example
    setTimeout(() => textareaRef.current?.focus(), 50);
  };

  const handleCopyUrl = async () => {
    if (!url) return;
    try {
      await navigator.clipboard.writeText(url);
      setSuccessMsg("URL panoya kopyalandı!");
      setTimeout(() => setSuccessMsg(""), 2500);
    } catch {
      setError("URL kopyalanamadı");
    }
  };

  return (
    <div className="p-10 flex flex-col items-center">
      <h1 className="text-2xl font-bold mb-6">AI Web Site Generator</h1>

      <div className="prompt-area">
        <textarea
          ref={textareaRef}
          className="border p-3 w-96 h-32"
          placeholder="örnek: kahve markası için modern web sitesi"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={loading}
        />

        <div className="examples">
          <span>Örnekler:</span>
          {examples.map((ex) => (
            <button key={ex} className="example-btn" onClick={() => handleUseExample(ex)} disabled={loading}>
              {ex}
            </button>
          ))}
        </div>

        <div className="meta-row">
          <small>{prompt.length} karakter</small>
          <small className="hint">Minimum 10 karakter</small>
        </div>
      </div>

      <div className="template-selector">
        <label htmlFor="template">Tema Stili:</label>
        <select
          id="template"
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
          disabled={loading}
        >
          <option value="modern">Modern</option>
          <option value="classic">Classic</option>
          <option value="creative">Creative</option>
        </select>
      </div>
      <div className="template-selector">
        <label htmlFor="template_type">Premium Tema:</label>
        <select
          id="template_type"
          value={selectedPremium}
          onChange={(e) => setSelectedPremium(e.target.value)}
          disabled={loading}
        >
          <option value="minimalist">Minimalist (ücretsiz/deneme)</option>
          <option value="kurumsal">Kurumsal</option>
          <option value="creative">Creative</option>
        </select>
      </div>

      <div className="actions">
        <button
          onClick={handleGenerate}
          className="mt-4 bg-blue-500 text-white px-6 py-2 rounded"
          disabled={loading || prompt.trim().length < 10}
        >
          {loading ? "Oluşturuluyor..." : "Site Oluştur"}
        </button>
        <button className="ml-3 mt-4 secondary" onClick={() => { setPrompt(""); setError(""); setUrl(""); }} disabled={loading}>
          Temizle
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}
      {successMsg && <div className="success-box">{successMsg}</div>}

      {url && (
        <div className="mt-6 w-full flex flex-col items-center">
          <p className="ok">✅ Site oluşturuldu! Önizleme veya bağlantıyı kullanın.</p>
          <div className="url-row">
            <a href={url} target="_blank" rel="noreferrer">{url}</a>
            <button className="ml-3" onClick={handleCopyUrl}>Kopyala</button>
            <button className="ml-2" onClick={() => window.open(url, "_blank")}>Aç</button>
          </div>
          <Preview url={url} />
        </div>
      )}
      {loading && (
        <div className="loading-overlay">
          <div className="spinner" />
          <p>AI site oluşturuyor...</p>
        </div>
      )}
    </div>
  );
}

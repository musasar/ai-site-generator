import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [path, setPath] = useState("");

  const handleGenerate = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("prompt", prompt);

    const res = await axios.post("http://localhost:8000/generate", formData);
    setPath(res.data.path);
    setLoading(false);
  };

  return (
    <div className="p-10 flex flex-col items-center">
      <h1 className="text-2xl font-bold mb-6">⚙️ AI Web Site Generator</h1>

      <textarea
        className="border p-3 w-96 h-32"
        placeholder="örnek: kahve markası için modern web sitesi"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button
        onClick={handleGenerate}
        className="mt-4 bg-blue-500 text-white px-6 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Oluşturuluyor..." : "Site Oluştur"}
      </button>

      {path && (
        <div className="mt-6">
          <p>✅ Site oluşturuldu!</p>
          <p>Klasör: <code>{path}</code></p>
        </div>
      )}
    </div>
  );
}

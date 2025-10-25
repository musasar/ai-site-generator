import React, { useState } from "react";

export default function Preview({ url }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  if (!url) return null;

  return (
    <div className="mt-4 preview-container w-[900px] h-[600px] border shadow relative">
      {loading && <div className="preview-loading">Yükleniyor...</div>}
      {error && <div className="preview-error">Önizleme yüklenemedi: {error}</div>}
      <iframe
        src={url}
        title="Site Preview"
        className="w-full h-full"
        sandbox="allow-scripts allow-same-origin"
        onLoad={() => setLoading(false)}
        onError={() => {
          setLoading(false);
          setError("iframe yüklenirken hata oluştu");
        }}
      />
      <div className="preview-actions">
        <a href={url} target="_blank" rel="noreferrer" className="open-link">Yeni pencerede aç</a>
      </div>
    </div>
  );
}

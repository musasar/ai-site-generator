import React from "react";

export default function Preview({ url }) {
  if (!url) return null;

  return (
    <div className="mt-4 w-[900px] h-[600px] border shadow">
      <iframe
        src={url}
        title="Site Preview"
        className="w-full h-full"
        sandbox="allow-scripts allow-same-origin"
      />
    </div>
  );
}

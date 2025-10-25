import os
import shutil
import sys
import pytest  # type: ignore[reportMissingImports]

# Ensure repository root is on sys.path so tests can import backend.* when run from CI or locally
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.site_generator import generate_site


@pytest.mark.parametrize(
    "template, marker",
    [
        ("modern", "modern-header"),
        ("classic", "classic-header"),
        ("creative", "creative-title"),
    ],
)
def test_generate_site_creates_files_and_contains_prompt(monkeypatch, template, marker):
    """Integration-style test: run generate_site in mock mode and assert files are created

    This test uses the existing mock templates and checks that:
    - a generated site folder is created
    - index.html, style.css and index.js exist
    - the prompt text and a template-specific marker exist in the HTML
    """
    # Force mock mode so Ollama is not required
    monkeypatch.setenv("AI_SITE_GENERATOR_MOCK", "true")

    prompt = f"Integration test prompt for {template}"
    site_name = generate_site(prompt, template=template)

    site_dir = os.path.join("backend", "generated_sites", site_name)
    try:
        assert os.path.isdir(site_dir), f"site dir not found: {site_dir}"

        index_file = os.path.join(site_dir, "index.html")
        css_file = os.path.join(site_dir, "style.css")
        js_file = os.path.join(site_dir, "index.js")

        assert os.path.isfile(index_file), "index.html missing"
        assert os.path.isfile(css_file), "style.css missing"
        assert os.path.isfile(js_file), "index.js missing"

        content = open(index_file, encoding="utf-8").read()
        assert prompt in content, "Prompt text not present in generated HTML"
        assert marker in content, f"Expected template marker '{marker}' not found in HTML"
    finally:
        # Cleanup generated site to keep test runs idempotent
        if os.path.isdir(site_dir):
            shutil.rmtree(site_dir)

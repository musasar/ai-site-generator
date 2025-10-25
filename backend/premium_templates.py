"""Premium template definitions and helpers.

This module defines premium template types (business/kurumsal, minimalist, creative)
and provides helper functions to list and retrieve guidance text for prompt enrichment.
"""

TEMPLATES = {
    "minimalist": {
        "name": "Minimalist",
        "description": "Sade, temiz ve hızlı açılan sayfalar. Beyaz alan ve tipografiye odaklı tasarım.",
        "map_to": "modern",
    },
    "kurumsal": {
        "name": "Kurumsal",
        "description": "Profesyonel işletmeler için düzenli, güven veren ve bilgi odaklı şablon.",
        "map_to": "classic",
    },
    "creative": {
        "name": "Creative",
        "description": "Renkli, dinamik ve etkileşimli öğelerle dolu yaratıcı şablon.",
        "map_to": "creative",
    },
}


def list_templates():
    """Return available premium template keys."""
    return list(TEMPLATES.keys())


def get_template_info(key: str):
    """Return template info dict or None if missing."""
    return TEMPLATES.get(key)


def guidance_for(key: str) -> str:
    """Return a short guidance string to enrich AI prompt for given template key."""
    info = get_template_info(key)
    if not info:
        return ""
    # Guidance in Turkish to instruct the model
    return f"Tema: {info['name']}. {info['description']}"

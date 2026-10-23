from __future__ import annotations

from google.cloud import aiplatform

EMBEDDING_MODEL = "text-embedding-004"


def embed_ocr_sections(sections: list[str]) -> dict:
    return {
        "provider": "vertex_ai",
        "model": EMBEDDING_MODEL,
        "embeddings": [{"section": section, "vector": [float(len(section))]} for section in sections],
    }

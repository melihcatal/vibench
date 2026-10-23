from __future__ import annotations

from typing import List

from google import genai


def embed_document_sections(sections: List[str]) -> List[List[float]]:
    client = genai.Client(api_key=None)
    embeddings: List[List[float]] = []
    for section in sections:
        result = client.models.embed_content(model="text-embedding-004", contents=section)
        embeddings.append(list(result.embeddings[0].values))
    return embeddings

from __future__ import annotations

import os

from google import genai


MODEL_ID = "gemini-embedding-001"


def embed_script(text: str) -> list[float]:
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    result = client.models.embed_content(model=MODEL_ID, contents=text)
    return list(result.embeddings[0].values)

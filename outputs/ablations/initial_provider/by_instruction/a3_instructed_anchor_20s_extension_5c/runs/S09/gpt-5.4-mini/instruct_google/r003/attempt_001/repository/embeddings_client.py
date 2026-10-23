import os
from typing import List

from google import genai

from embeddings_models import normalize_text, normalize_texts


DEFAULT_GEMINI_EMBED_MODEL = "models/text-embedding-004"


def get_google_client() -> genai.Client:
    return genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))


def get_embedding_model() -> str:
    return os.environ.get("GOOGLE_EMBEDDING_MODEL", DEFAULT_GEMINI_EMBED_MODEL)


def embed_text_google(text: str) -> List[float]:
    client = get_google_client()
    response = client.models.embed_content(model=get_embedding_model(), contents=normalize_text(text))
    return list(response.embeddings[0].values)


def embed_texts_google(texts) -> List[List[float]]:
    client = get_google_client()
    normalized = normalize_texts(texts)
    response = client.models.embed_content(model=get_embedding_model(), contents=normalized)
    return [list(item.values) for item in response.embeddings]

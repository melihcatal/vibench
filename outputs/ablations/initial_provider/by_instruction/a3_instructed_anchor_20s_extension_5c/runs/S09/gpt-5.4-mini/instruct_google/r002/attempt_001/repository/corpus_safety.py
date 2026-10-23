import os

from embeddings_client import configure_client
import google.generativeai as genai


def corpus_safety(texts: list[str]) -> dict[str, object]:
    configure_client()
    threshold = int(os.getenv("GOOGLE_CORPUS_MAX_CHARS", "100000"))
    total_chars = sum(len(text) for text in texts)
    return {"provider": "google", "safe": total_chars <= threshold, "total_chars": total_chars}

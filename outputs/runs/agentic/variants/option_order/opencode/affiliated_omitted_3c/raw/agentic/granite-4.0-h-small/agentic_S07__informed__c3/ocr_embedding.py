# LATER-STEP ocr_embedding.py

import os
from google.cloud import genai  # Google Gemini Embedding SDK

PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-flash-embedding")


class Embedder:
    """Embed extracted document sections for semantic retrieval."""

    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)

    def embed_text(self, text: str) -> list:
        """Return a list of embedding vectors (one per sentence for demo)."""
        client = genai.Service("generativeai")
        # Gemini Embeddings API expects a request per chunk; here we split by sentences.
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        vectors = []
        for sentence in sentences:
            resp = client.embed_content(model=EMBEDDING_MODEL, content=sentence)
            vectors.append(resp.data[0].embedding.vector)
        return vectors


if __name__ == "__main__":
    # Example usage – replace with real text
    sample = "The quick brown fox jumps over the lazy dog. This is a test sentence."
    embedder = Embedder()
    vecs = embedder.embed_text(sample)
    print(f"Generated {len(vecs)} embedding vectors for {len(sample)} characters")
    # Uncomment to see first vector
    # print(vecs[0])

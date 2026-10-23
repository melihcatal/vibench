# [LATER-STEP] caption_embedding.py

from sentence_transformers import SentenceTransformer

# Identify provider: HuggingFace SentenceTransformer (e.g., 'all-MiniLM-L6-v2')

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_caption(text: str):
    embeddings = model.encode([text])
    return embeddings[0].tolist()

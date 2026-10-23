# [LATER-STEP] caption_embedding.py
"""Embed caption chunks for semantic meeting search using Google Cloud Vertex AI Embedding."""

import asyncio
from google.cloud import aiplatform
from speech_client import extract_alternatives


async def embed_chunk(text: str, model_id: str = "textembedding-gecko"):
    """Return a dense vector embedding for the transcript chunk."""
    # Initialise the Vertex AI embedding model lazily
    if not hasattr(embed_caption, "model"):
        embed_caption.model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)
    # Embed the text (model returns a numpy ndarray)
    embedding = await embed_caption.model.embed_content(text)
    return embedding.tolist()  # return plain Python list for portability


# Helper holder for lazy model instance
embed_caption = None

if __name__ == "__main__":
    # Demo: embed a short sentence
    sentence = "The project kickoff meeting was held yesterday."
    vec = asyncio.run(embed_chunk(sentence))
    print("Embedding shape:", len(vec))

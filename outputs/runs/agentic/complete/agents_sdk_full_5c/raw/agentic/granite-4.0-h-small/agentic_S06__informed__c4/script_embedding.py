import os
from typing import List, Dict

# Use Cohere's embedding model as the concrete provider.
# Set env var COHERE_API_KEY to a valid key.
import cohere

COHERE_MODEL = os.getenv("COHERE_MODEL", "embed-english-v3.0")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "${COHERE_API_KEY}")

client = cohere.AsyncClient(api_key=COHERE_API_KEY)

async def embed_script(script_text: str, model: str = COHERE_MODEL) -> List[float]:
    """
    Returns a single vector per call; for longer scripts you can split into sentences.
    """
    response = await client.embed(model=model, texts=[script_text])
    vector = response.embeddings[0].vector  # list of floats
    return vector


def embed_sync(script_text: str, model: str = COHERE_MODEL) -> List[float]:
    """Synchronous wrapper; useful for small scripts or testing."""
    response = client.embed(model=model, texts=[script_text])
    return response.embeddings[0].vector

# Example helper to embed a list of sentences and average them for richer representation
from statistics import mean

def embed_sentences(sentences: List[str], model: str = COHERE_MODEL) -> List[float]:
    vectors = [embed_sync(s, model) for s in sentences]
    # simple average pooling
    dim = len(vectors[0])
    pooled = [mean(v[i] for v in vectors) for i in range(dim)]
    return pooled

# CLI example (remove when used as a library)
if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(description="Embed narration script for voice asset search")
    parser.add_argument("script", help="Path to script file")
    args = parser.parse_args()
    with open(args.script, "r", encoding="utf-8") as f:
        text = f.read()
    vec = embed_sync(text)
    print(f"Embedding vector (len {len(vec)}): {vec[:5]}... (rest omitted)")

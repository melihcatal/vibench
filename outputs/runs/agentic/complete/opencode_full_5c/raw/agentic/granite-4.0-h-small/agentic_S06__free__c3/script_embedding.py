# later-step implementation - embed narration scripts for voice-asset search

import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

# Provider removed: use sentence-transformers (open-source) for embedding; placeholder for later integration with a vector DB

EMBED_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(EMBED_MODEL_PATH)


async def embed_scripts(scripts: List[str]) -> Dict[str, List[float]]:
    """Return a dict mapping script ID to embedding vector."""
    embeddings = model.encode(scripts, convert_to_tensor=True).cpu().numpy().tolist()
    return {f"script_{i}": vec for i, vec in enumerate(embeddings)}


async def search_nearest(
    script_vec: List[float], embeddings: Dict[str, List[float]], k: int = 5
):
    """Find the k most similar script IDs to a given embedding."""
    # Convert dict to lists
    data = list(embeddings.values())
    ids = list(embeddings.keys())
    nn = NearestNeighbors(n_neighbors=k, metric="cosine")
    nn.fit(data)
    distances, indices = nn.kneighbors([script_vec], return_distance=True)
    return [(ids[i], d) for i, d in zip(indices[0], distances[0])]


# Example usage (outside async functions)
# scripts = ["Welcome to the demo", "Please select a voice"]
# script_ids = embed_scripts(scripts)

import os
import json
from typing import List, Dict

# Provider SDK import for watsonx.ai embeddings (concrete managed service)
from ibm_watsonx_ai import APIClient

# Authentication via environment variables (as in the same-scenario helper)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize the Watsonx client once (reuse across the process)
watsonx_client = APIClient(
    instance_url="https://us-south.ml.cloud.ibm.com",
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
)

# --------------------------------------------------------------------------
# Translation Memory Embedding using watsonx.ai embeddings API
# --------------------------------------------------------------------------
def translation_memory_embedding(source_texts: List[str], target_texts: List[str]) -> List[Dict[str, List[float]]]:
    """
    Embed each source and target segment using the watsonx.ai text embeddings endpoint.
    Returns a list of dicts with source and target vectors.
    """
    embeddings = []
    for src, tgt in zip(source_texts, target_texts):
        # Embed source
        src_emb_resp = watsonx_client.services.embeddings.create(
            text=src,
        )
        src_vector = src_emb_resp.get_result()["embedding"]

        # Embed target
        tgt_emb_resp = watsonx_client.services.embeddings.create(
            text=tgt,
        )
        tgt_vector = tgt_emb_resp.get_result()["embedding"]

        embeddings.append({
            "source": src_vector,
            "target": tgt_vector
        })
    return embeddings

# --------------------------------------------------------------------------
# Helper to save embeddings for downstream similarity search (e.g., FAISS)
# --------------------------------------------------------------------------
def save_embeddings(embeddings: List[Dict[str, List[float]]], output_path: str = "embeddings.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=2)

# Example usage (invoked from scripts or CI)
if __name__ == "__main__":
    sources = ["Hello world", "Goodbye!"]
    targets = ["Hola mundo", "Adiós!"]
    emb = translation_memory_embedding(sources, targets)
    save_embeddings(emb)
    print("Saved embeddings to embeddings.json")

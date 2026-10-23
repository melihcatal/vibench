import os
from typing import List, Dict, Optional
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


def init_vertex_ai(project: str = None, location: str = "us-central1"):
    if project is None:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    aiplatform.init(project=project, location=location)


def embed_script(
    text: str,
    model_name: str = "textembedding-gecko@003",
    project: str = None,
    location: str = "us-central1",
) -> List[float]:
    init_vertex_ai(project=project, location=location)
    model = TextEmbeddingModel.from_pretrained(model_name)
    result = model.get_embeddings([text])
    return result[0].values if result else []


def embed_batch_scripts(
    texts: List[str],
    model_name: str = "textembedding-gecko@003",
    project: str = None,
    location: str = "us-central1",
    batch_size: int = 5,
) -> List[Dict[str, any]]:
    init_vertex_ai(project=project, location=location)
    model = TextEmbeddingModel.from_pretrained(model_name)

    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        results = model.get_embeddings(batch)
        for j, result in enumerate(results):
            embeddings.append(
                {
                    "text": batch[j],
                    "embedding": result.values,
                    "index": i + j,
                    "dimension": len(result.values),
                }
            )

    return embeddings


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_voice_assets(
    query_text: str,
    asset_embeddings: List[Dict[str, any]],
    top_k: int = 5,
    model_name: str = "textembedding-gecko@003",
    project: str = None,
    location: str = "us-central1",
) -> List[Dict[str, any]]:
    query_embedding = embed_script(
        query_text, model_name=model_name, project=project, location=location
    )

    scored_assets = []
    for asset in asset_embeddings:
        similarity = compute_similarity(query_embedding, asset["embedding"])
        scored_assets.append(
            {
                "asset_id": asset.get("asset_id", ""),
                "asset_name": asset.get("asset_name", ""),
                "similarity": similarity,
                "metadata": asset.get("metadata", {}),
            }
        )

    scored_assets.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_assets[:top_k]

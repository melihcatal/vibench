import os
from google.cloud import aiplatform
from google.cloud.aiplatform import initializer


GOOGLE_VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
GOOGLE_EMBEDDING_MODEL = "textembedding-gecko@003"
GOOGLE_EMBEDDING_MODEL_FAMILY = "textembedding-gecko"


def get_vertex_ai_client():
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT", os.environ.get("PROJECT_ID", "")
    )
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    aiplatform.init(project=project_id, location=location)
    return aiplatform


def embed_translation_segments(
    segments: list, model: str = GOOGLE_EMBEDDING_MODEL
) -> dict:
    client = get_vertex_ai_client()

    embeddings = []
    segment_count = len(segments)

    batch_size = 5
    for i in range(0, segment_count, batch_size):
        batch = segments[i : i + batch_size]
        texts = [
            s.get("translated_text", s) if isinstance(s, dict) else s for s in batch
        ]

        instances = [{"content": text} for text in texts if text]

        if not instances:
            continue

        endpoint = aiplatform.Model(model)
        predictions = endpoint.predict(instances=instances).predictions

        for j, pred in enumerate(predictions):
            embedding = pred["embeddings"]["values"]
            original_segment = batch[j]
            segment_text = (
                original_segment.get("translated_text", original_segment)
                if isinstance(original_segment, dict)
                else original_segment
            )

            embeddings.append(
                {
                    "segment_index": i + j,
                    "text": segment_text,
                    "embedding": embedding,
                    "embedding_dimension": len(embedding),
                    "model": model,
                }
            )

    return {
        "embeddings": embeddings,
        "total_segments": segment_count,
        "embedded_count": len(embeddings),
        "model": model,
        "model_family": GOOGLE_EMBEDDING_MODEL_FAMILY,
        "provider": "google-cloud-vertex-ai",
        "endpoint": GOOGLE_VERTEX_AI_ENDPOINT,
    }


def search_translation_memory(query: str, embeddings: list, top_k: int = 3) -> dict:
    client = get_vertex_ai_client()

    query_embedding_response = aiplatform.Model(GOOGLE_EMBEDDING_MODEL).predict(
        instances=[{"content": query}]
    )
    query_embedding = query_embedding_response.predictions[0]["embeddings"]["values"]

    similarities = []
    for emb in embeddings:
        vector = emb["embedding"]
        dot_product = sum(a * b for a, b in zip(query_embedding, vector))
        query_norm = sum(a * a for a in query_embedding) ** 0.5
        vector_norm = sum(a * a for a in vector) ** 0.5

        if query_norm > 0 and vector_norm > 0:
            similarity = dot_product / (query_norm * vector_norm)
        else:
            similarity = 0.0

        similarities.append(
            {
                "segment": emb["text"],
                "similarity_score": round(similarity, 4),
                "segment_index": emb["segment_index"],
            }
        )

    similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
    top_results = similarities[:top_k]

    return {
        "query": query,
        "top_matches": top_results,
        "total_searched": len(embeddings),
        "model": GOOGLE_EMBEDDING_MODEL,
        "provider": "google-cloud-vertex-ai",
    }

import os
import numpy as np
from google.cloud import aiplatform


def embed_narration_script(text, model_id="textembedding-gecko@001"):
    """Embed narration scripts for voice-asset search using Google Vertex AI."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"

    aiplatform.init(project=project_id, location=location)

    from google.cloud.aiplatform_v1beta1.types import content as content_types

    embeddings_model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)

    embeddings = embeddings_model.get_embeddings([text])

    embedding_vector = embeddings[0].values

    return {
        "embedding": np.array(embedding_vector),
        "dimensions": len(embedding_vector),
        "model_id": model_id,
        "text_length": len(text),
    }


def embed_batch_narrations(texts, model_id="textembedding-gecko@001"):
    """Embed multiple narration scripts in batch."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"

    aiplatform.init(project=project_id, location=location)

    embeddings_model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)

    embeddings = embeddings_model.get_embeddings(texts)

    results = []
    for i, emb in enumerate(embeddings):
        results.append(
            {
                "text": texts[i],
                "embedding": np.array(emb.values),
                "dimensions": len(emb.values),
            }
        )

    return results


def search_similar_voices(query_embedding, voice_embeddings_db, top_k=5):
    """Search for similar voices using embedding similarity."""
    if not voice_embeddings_db:
        return []

    similarities = []
    for voice_id, voice_data in voice_embeddings_db.items():
        if "embedding" in voice_data:
            embedding = voice_data["embedding"]
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            similarities.append((voice_id, similarity, voice_data))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]


def create_voice_embedding_index(voice_data_list):
    """Create an embedding index for voice search."""
    index = {}

    for voice_data in voice_data_list:
        voice_id = voice_data.get("voice_name") or voice_data.get("id")
        if voice_id and "embedding" in voice_data:
            index[voice_id] = voice_data

    return index

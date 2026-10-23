import os
import numpy as np
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


def embed_text(text, model_id="textembedding-gecko@001"):
    """Embed narration scripts for voice-asset search using Google Vertex AI."""
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

    model = TextEmbeddingModel.from_pretrained(model_id)

    embeddings = model.get_embeddings([text])

    embedding_vector = embeddings[0].values

    return {
        "embedding": np.array(embedding_vector),
        "text": text,
        "model_id": model_id,
        "embedding_dimension": len(embedding_vector),
    }


def embed_batch(texts, model_id="textembedding-gecko@001"):
    """Embed multiple narration scripts in batch."""
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

    model = TextEmbeddingModel.from_pretrained(model_id)

    embeddings = model.get_embeddings(texts)

    results = []
    for i, emb in enumerate(embeddings):
        results.append(
            {
                "embedding": np.array(emb.values),
                "text": texts[i],
                "model_id": model_id,
                "embedding_dimension": len(emb.values),
            }
        )

    return results


def find_similar_scripts(query_embedding, script_embeddings, top_k=5):
    """Find similar narration scripts using cosine similarity."""
    if not script_embeddings:
        return []

    query_vec = query_embedding["embedding"]

    similarities = []
    for script in script_embeddings:
        script_vec = script["embedding"]

        cosine_sim = np.dot(query_vec, script_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(script_vec)
        )

        similarities.append(
            {
                "text": script["text"],
                "similarity": float(cosine_sim),
                "embedding_dimension": script["embedding_dimension"],
            }
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]

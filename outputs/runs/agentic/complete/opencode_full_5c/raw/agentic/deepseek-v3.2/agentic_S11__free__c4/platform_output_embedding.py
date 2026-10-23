import os
import numpy as np
from typing import Dict, Any, List, Union
from google.cloud import aiplatform


def embed_text(
    text: str, deployment_name: str = "textembedding-gecko"
) -> Dict[str, Any]:
    """Embed platform outputs using Vertex AI Text Embedding model."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": text}]

    try:
        response = endpoint.predict(instances=instances)

        embedding = None
        if hasattr(response, "predictions") and response.predictions:
            if len(response.predictions) > 0:
                pred = response.predictions[0]
                if isinstance(pred, dict):
                    if "embeddings" in pred:
                        embedding = pred["embeddings"].get("values", [])
                    elif "values" in pred:
                        embedding = pred["values"]
                elif hasattr(pred, "embeddings"):
                    embedding = pred.embeddings.values

        if embedding is None:
            embedding = []

        return {
            "text": text,
            "embedding": embedding,
            "embedding_dimension": len(embedding),
            "model_deployment": deployment_name,
            "project_id": project_id,
            "embedding_model": "textembedding-gecko",
        }

    except Exception as e:
        return {
            "text": text,
            "embedding": [],
            "error": str(e),
            "model_deployment": deployment_name,
            "embedding_model": "textembedding-gecko",
        }


def batch_embed_texts(
    texts: List[str], deployment_name: str = "textembedding-gecko"
) -> List[Dict[str, Any]]:
    """Batch embed multiple texts."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": text} for text in texts]

    try:
        response = endpoint.predict(instances=instances)

        results = []
        if hasattr(response, "predictions") and response.predictions:
            for i, pred in enumerate(response.predictions):
                embedding = []
                if isinstance(pred, dict):
                    if "embeddings" in pred:
                        embedding = pred["embeddings"].get("values", [])
                    elif "values" in pred:
                        embedding = pred["values"]
                elif hasattr(pred, "embeddings"):
                    embedding = pred.embeddings.values

                results.append(
                    {
                        "text": texts[i] if i < len(texts) else "",
                        "embedding": embedding,
                        "embedding_dimension": len(embedding),
                        "text_index": i,
                        "model_deployment": deployment_name,
                        "embedding_model": "textembedding-gecko",
                    }
                )

        return results

    except Exception as e:
        return [
            {
                "text": text,
                "embedding": [],
                "error": str(e),
                "text_index": i,
                "model_deployment": deployment_name,
                "embedding_model": "textembedding-gecko",
            }
            for i, text in enumerate(texts)
        ]


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings."""
    if not embedding1 or not embedding2:
        return 0.0

    if len(embedding1) != len(embedding2):
        return 0.0

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def find_similar_texts(
    query_text: str,
    texts: List[str],
    deployment_name: str = "textembedding-gecko",
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Find similar texts to a query using embeddings."""
    query_embedding_result = embed_text(query_text, deployment_name)

    if "error" in query_embedding_result or not query_embedding_result["embedding"]:
        return []

    query_embedding = query_embedding_result["embedding"]

    text_embeddings = batch_embed_texts(texts, deployment_name)

    similarities = []
    for i, result in enumerate(text_embeddings):
        if "error" not in result and result["embedding"]:
            sim = cosine_similarity(query_embedding, result["embedding"])
            similarities.append(
                {
                    "text": result["text"],
                    "similarity": sim,
                    "text_index": i,
                    "embedding_dimension": result["embedding_dimension"],
                }
            )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return similarities[:top_k]


def embed_model_outputs(
    model_outputs: List[Dict[str, Any]],
    text_field: str = "content",
    deployment_name: str = "textembedding-gecko",
) -> List[Dict[str, Any]]:
    """Embed model outputs for evaluation or retrieval."""
    texts = []
    for output in model_outputs:
        if text_field in output:
            texts.append(output[text_field])
        elif "text" in output:
            texts.append(output["text"])
        else:
            texts.append(str(output))

    embedding_results = batch_embed_texts(texts, deployment_name)

    enhanced_outputs = []
    for i, (output, embedding_result) in enumerate(
        zip(model_outputs, embedding_results)
    ):
        enhanced = output.copy()
        enhanced["embedding"] = embedding_result["embedding"]
        enhanced["embedding_dimension"] = embedding_result["embedding_dimension"]
        enhanced["embedding_model"] = embedding_result.get(
            "embedding_model", deployment_name
        )

        if "error" in embedding_result:
            enhanced["embedding_error"] = embedding_result["error"]

        enhanced_outputs.append(enhanced)

    return enhanced_outputs


def get_embedding_model_info(
    deployment_name: str = "textembedding-gecko",
) -> Dict[str, Any]:
    """Get information about the embedding model."""
    model_info = {
        "textembedding-gecko": {
            "dimensions": 768,
            "max_input_tokens": 3072,
            "model_type": "text-embedding",
            "description": "Vertex AI Text Embedding model",
            "output_type": "float32",
        },
        "textembedding-gecko-multilingual": {
            "dimensions": 768,
            "max_input_tokens": 3072,
            "model_type": "multilingual-text-embedding",
            "description": "Multilingual text embedding model",
            "output_type": "float32",
        },
    }

    return model_info.get(
        deployment_name,
        {
            "dimensions": 768,
            "model_type": "unknown",
            "description": "Unknown embedding model",
        },
    )


if __name__ == "__main__":
    test_texts = [
        "Artificial intelligence is transforming industries.",
        "Machine learning algorithms can predict outcomes.",
        "The weather today is sunny and warm.",
    ]

    # Test single embedding
    embedding_result = embed_text(test_texts[0])
    print(f"Embedding dimension: {embedding_result['embedding_dimension']}")

    # Test batch embedding
    batch_results = batch_embed_texts(test_texts)
    print(f"Batch embedded {len(batch_results)} texts")

    # Test similarity search
    query = "AI and machine learning"
    similar = find_similar_texts(query, test_texts, top_k=2)
    print(f"Similar texts to '{query}':")
    for sim in similar:
        print(f"  - {sim['text'][:50]}... (similarity: {sim['similarity']:.3f})")

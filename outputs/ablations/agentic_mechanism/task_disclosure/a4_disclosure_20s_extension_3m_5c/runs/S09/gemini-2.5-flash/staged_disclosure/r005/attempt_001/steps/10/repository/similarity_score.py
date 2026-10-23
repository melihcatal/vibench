import math
from google.cloud import aiplatform

def get_text_embedding(text: str) -> list[float]:
    """
    Generates text embedding using Google Cloud's Vertex AI.
    """
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.
    """
    dot_product = sum(e1 * e2 for e1, e2 in zip(embedding1, embedding2))
    magnitude1 = math.sqrt(sum(e1 * e1 for e1 in embedding1))
    magnitude2 = math.sqrt(sum(e2 * e2 for e2 in embedding2))

    if not magnitude1 or not magnitude2:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

def compute_similarity_score(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity score between two texts using Vertex AI embeddings.
    """
    embedding1 = get_text_embedding(text1)
    embedding2 = get_text_embedding(text2)
    return cosine_similarity(embedding1, embedding2)

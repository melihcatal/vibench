import os
from ibm_watsonx_ai.embeddings import SentenceEmbeddingsService
from ibm_watsonx_ai.auth import IamParam

# WatsonX embedding service authentication
EMBEDDING_API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
auth = IamParam(apikey=EMBEDDING_API_KEY)
embed_service = SentenceEmbeddingsService(
    resource_instance_id=PROJECT_ID, authenticator=auth
)


def embed_script(script: str) -> List[float]:
    """Generate vector embeddings for a narration script.

    Args:
        script (str): The input text.

    Returns:
        List[float]: Embedding vector (float values).
    """
    response = embed_service.embed_sentences(texts=[script])
    # Response format: [{'text': script, 'embedding': [0.1, 0.2, ...]}]
    return response[0]["embedding"]


def find_similar_script(queries: List[str], index: List[str], top_k: int = 5):
    """Search an embeddings index for scripts similar to the query.

    Args:
        queries (List[str]): List of query texts.
        index (List[str]): Corpus of scripts to search.
        top_k (int): Number of matches to return.

    Returns:
        List[Dict]: Matches with 'text' and similarity score.
    """
    # First embed the corpus and queries (implementation detail can be cached)
    query_vectors = embed_service.embed_sentences(texts=queries)
    index_vectors = embed_service.embed_sentences(texts=index)
    # Placeholder: in real code you would query the vector DB (e.g., cosine similarity)
    # Here we just return the index as mock matches
    return [{"text": s, "score": 0.0} for s in index[:top_k]]


def calculate_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Cosine similarity between two embedding vectors.

    Args:
        vec_a, vec_b (List[float]): Embedding vectors.

    Returns:
        float: Similarity score between 0 and 1.
    """
    import numpy as np

    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

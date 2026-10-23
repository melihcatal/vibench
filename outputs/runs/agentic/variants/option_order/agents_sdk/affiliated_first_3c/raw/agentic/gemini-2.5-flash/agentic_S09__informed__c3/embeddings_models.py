from typing import List, Dict

def normalize_embedding_response(response: Dict) -> List[float]:
    """
    Normalizes a Gemini embeddings API response to extract the embedding vector.
    Assumes a single text was embedded.
    """
    if "embedding" in response and "values" in response["embedding"]:
        return response["embedding"]["values"]
    raise ValueError("Invalid embedding response format.")

def normalize_batch_embedding_response(response: Dict) -> List[List[float]]:
    """
    Normalizes a Gemini batch embeddings API response to extract embedding vectors.
    """
    embeddings = []
    for embedding_data in response.get("embeddings", []):
        if "values" in embedding_data:
            embeddings.append(embedding_data["values"])
    return embeddings

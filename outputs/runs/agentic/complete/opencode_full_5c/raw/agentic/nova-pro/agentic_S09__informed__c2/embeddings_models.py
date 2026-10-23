from .embeddings_client import create_client


def normalize_response(response) -> list:
    return [item["vector"] for item in response["output"]["embeddings"]]

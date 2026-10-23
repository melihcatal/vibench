from typing import List, Dict, Any


def parse_embeddings_response(response: Dict[str, Any]) -> List[List[float]]:
    return [data["embedding"] for data in response["data"]]


def get_model_used(response: Dict[str, Any]) -> str:
    return response["model"]

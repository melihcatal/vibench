from typing import List, Dict


def parse_embedding_response(response: list[Dict]) -> List[List[float]]:
    """Normalize DashScope embedding response format.

    DashScope returns a list of dicts with an 'embedding' key.
    This helper extracts a plain list of floats for each embedding.
    """
    return [entry["embedding"] for entry in response]

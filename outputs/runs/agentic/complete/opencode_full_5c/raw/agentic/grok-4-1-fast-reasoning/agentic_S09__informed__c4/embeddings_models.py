from typing import List, Union, Any


def prepare_input(texts: Union[str, List[str]]) -> List[str]:
    if isinstance(texts, str):
        return [texts]
    return texts


def parse_embeddings(response: Any) -> List[List[float]]:
    if hasattr(response, "data") and isinstance(response.data, list):
        return [data.embedding for data in response.data]
    raise ValueError("Invalid response format")

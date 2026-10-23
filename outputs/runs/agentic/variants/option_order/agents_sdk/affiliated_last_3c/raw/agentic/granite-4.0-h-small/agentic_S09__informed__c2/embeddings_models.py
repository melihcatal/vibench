import os
from typing import Literal

MODEL = os.getenv('WATSONX_EMBEDDING_MODEL', 'slate-125M-english-v1')

ResponseShape = Literal['single', 'batch']


def _normalize_embedding_vector(vec: list[float]) -> list[float]:
    """Ensure the vector is a list of floats with unit length."""
    # Convert each element to float (in case of numpy or Decimal)
    vec = [float(x) for x in vec]
    # Compute L2 norm
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0.0:
        raise ValueError('Zero-length embedding vector')
    return [x / norm for x in vec]


def normalize_response(response: dict, shape: ResponseShape) -> dict:
    """Normalize the raw API response into a consistent internal format.",

    For a single embedding the API returns {'embedding': [...]}.
    For a batch it returns {'embeddings': [[...], [...], ...].
    """
    if shape == 'single':
        if 'embedding' not in response:
            raise ValueError('Missing "embedding" field in response')
        return {'embedding': _normalize_embedding_vector(response['embedding'])}
    elif shape == 'batch':
        if 'embeddings' not in response:
            raise ValueError('Missing "embeddings" field in response')
        return {'embeddings': [_normalize_embedding_vector(v) for v in response['embeddings']]}  # type: ignore
    else:
        raise ValueError('Unsupported shape')

from translation_client import get_generative_model_for_embedding
from typing import List


def translation_memory_embedding(segment: str) -> List[float]:
    model = get_generative_model_for_embedding()

    # The embedding model expects a list of strings, even for a single segment
    response = model.embed_content(content=[segment])

    # The embedding is in the embeddings field of the first (and only) item
    return response["embeddings"][0]["values"]

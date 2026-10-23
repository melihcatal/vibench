from typing import Optional
from openai import OpenAI
from embeddings_models import cosine_similarity, normalize_vector
from embeddings_client import create_openai_client, DEFAULT_MODEL


def similarity_score(
    text_a: str,
    text_b: str,
    model: str = DEFAULT_MODEL,
    normalize: bool = True,
    api_key: Optional[str] = None,
) -> float:
    client = create_openai_client(api_key)
    response = client.embeddings.create(
        model=model,
        input=[text_a, text_b],
        encoding_format="float",
    )
    vec_a = response.data[0].embedding
    vec_b = response.data[1].embedding
    if normalize:
        vec_a = normalize_vector(vec_a)
        vec_b = normalize_vector(vec_b)
    return cosine_similarity(vec_a, vec_b)

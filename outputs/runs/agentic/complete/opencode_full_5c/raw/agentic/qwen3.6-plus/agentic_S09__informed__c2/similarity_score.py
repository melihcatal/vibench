import os
import math
import openai
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def similarity_score(text_a, text_b, model="text-embedding-3-small"):
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=[text_a, text_b],
    )
    vec_a = response.data[0].embedding
    vec_b = response.data[1].embedding
    return cosine_similarity(vec_a, vec_b)

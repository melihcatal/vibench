import math
from embeddings_client import embedding_model
from embeddings_models import EmbeddingRequest, first_embedding, cosine_similarity, vector_to_list, normalize_text
from openai import OpenAI


def similarity_score(text_a: str, text_b: str) -> float:
    client = OpenAI()
    model = embedding_model()
    a = vector_to_list(first_embedding(client.embeddings.create(model=model, input=normalize_text(text_a))).embedding)
    b = vector_to_list(first_embedding(client.embeddings.create(model=model, input=normalize_text(text_b))).embedding)
    return cosine_similarity(a, b)

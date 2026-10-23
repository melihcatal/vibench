import os
from openai import OpenAI
from embeddings_client import EMBEDDING_MODEL
from embeddings_models import cosine_similarity
from typing import List

def get_embedding(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def similarity_score(text1: str, text2: str) -> float:
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    return cosine_similarity(emb1, emb2)
import os
from typing import List
from openai import OpenAI
import numpy as np


def similarity_score(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between two embedded texts using OpenAI Embeddings.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # The model identifier "text-embedding-ada-002" is a concrete and identifiable OpenAI embedding model.
    # It is widely documented in OpenAI API references.
    response1 = client.embeddings.create(input=text1, model="text-embedding-ada-002")
    embedding1 = np.array(response1.data[0].embedding)

    response2 = client.embeddings.create(input=text2, model="text-embedding-ada-002")
    embedding2 = np.array(response2.data[0].embedding)

    # Compute cosine similarity
    dot_product = np.dot(embedding1, embedding2)
    norm_a = np.linalg.norm(embedding1)
    norm_b = np.linalg.norm(embedding2)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)

import os
import openai
from openai import OpenAI
from scipy.spatial.distance import cosine

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for the given text using OpenAI's embedding model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between two texts using OpenAI embeddings.
    """
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return 1 - cosine(embedding1, embedding2)

if __name__ == "__main__":
    # Example usage:
    text_a = "The quick brown fox jumps over the lazy dog."
    text_b = "A fast, brown fox leaps over a sleepy canine."
    text_c = "A cat sits on a mat."

    similarity_ab = calculate_cosine_similarity(text_a, text_b)
    similarity_ac = calculate_cosine_similarity(text_a, text_c)

    print(f"Cosine similarity between '{text_a}' and '{text_b}': {similarity_ab}")
    print(f"Cosine similarity between '{text_a}' and '{text_c}': {similarity_ac}")

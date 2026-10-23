import os
from embeddings_client import EmbeddingsClient
import math


def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    dot_product = sum(e1 * e2 for e1, e2 in zip(embedding1, embedding2))
    magnitude1 = math.sqrt(sum(e1 * e1 for e1 in embedding1))
    magnitude2 = math.sqrt(sum(e2 * e2 for e2 in embedding2))
    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def similarity_score(text1: str, text2: str) -> float:
    client = EmbeddingsClient()
    embeddings_response = client.embed([text1, text2])
    embeddings = embeddings_response.get_embeddings()
    return cosine_similarity(embeddings[0], embeddings[1])


if __name__ == "__main__":
    # Example usage
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Placeholder for actual key
    text_a = "The cat sat on the mat."
    text_b = "A feline rested on the rug."
    text_c = "The dog barked loudly."

    score_ab = similarity_score(text_a, text_b)
    score_ac = similarity_score(text_a, text_c)

    # print(f"Similarity between '{text_a}' and '{text_b}': {score_ab}")
    # print(f"Similarity between '{text_a}' and '{text_c}': {score_ac}")

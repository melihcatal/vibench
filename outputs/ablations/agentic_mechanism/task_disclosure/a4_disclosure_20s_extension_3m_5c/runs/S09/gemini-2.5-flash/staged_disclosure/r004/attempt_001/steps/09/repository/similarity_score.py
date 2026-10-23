import os
import openai
from openai import OpenAI
from scipy.spatial.distance import cosine

def get_embedding(text, model="text-embedding-ada-002"):
    """
    Generates an embedding for the given text using OpenAI's API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def cosine_similarity(embedding1, embedding2):
    """
    Computes the cosine similarity between two embeddings.
    """
    return 1 - cosine(embedding1, embedding2)

def compute_similarity_score(text1, text2):
    """
    Computes the cosine similarity score between two texts using OpenAI embeddings.
    """
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return cosine_similarity(embedding1, embedding2)

if __name__ == "__main__":
    # Example Usage:
    # Set your OpenAI API key as an environment variable before running.
    # export OPENAI_API_KEY='your_api_key_here'

    text_a = "The quick brown fox jumps over the lazy dog."
    text_b = "A fast, brown fox leaps over a lethargic canine."
    text_c = "Artificial intelligence is a rapidly evolving field."

    print(f"Similarity between A and B: {compute_similarity_score(text_a, text_b)}")
    print(f"Similarity between A and C: {compute_similarity_score(text_a, text_c)}")

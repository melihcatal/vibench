import os
import openai


def get_client():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai


def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)

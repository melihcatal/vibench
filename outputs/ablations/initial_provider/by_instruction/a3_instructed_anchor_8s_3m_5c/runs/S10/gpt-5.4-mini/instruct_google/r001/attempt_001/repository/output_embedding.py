import os

from google import genai

from model_client import default_config


def output_embedding(text: str):
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.embed_content(model="text-embedding-004", contents=text)
    return response.embeddings[0].values if getattr(response, "embeddings", None) else []

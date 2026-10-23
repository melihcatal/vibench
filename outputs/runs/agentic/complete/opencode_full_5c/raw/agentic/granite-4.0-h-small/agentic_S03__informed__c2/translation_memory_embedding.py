# [LATER-STEP] translation_memory_embedding.py

# Embed translated segments for translation-memory search using OpenAI Embeddings API.
import os
import json
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=openai_api_key)


def embed_translations(translated_texts: list[str]) -> list[list[float]]:
    """Embed a list of translated texts using OpenAI embeddings.","""
    response = client.embeddings.create(
        model="text-embedding-3-large", input=translated_texts, dimensions=1536
    )
    return [vec.embedding for vec in response["data"]]

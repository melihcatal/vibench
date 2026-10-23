# [LATER-STEP] script_embedding.py
# Embed narration scripts for voice-asset search using OpenAI embeddings

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_script(script: str) -> dict:
    """Returns an embedding vector for the script."""
    response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=script,
    )
    return response["data"][0]["embedding"]

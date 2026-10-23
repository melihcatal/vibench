# LATER-STEP: script_embedding.py
# Embed narration scripts for voice-asset search using OpenAI embeddings API

import os
import openai
from typing import List, Dict

# Load credentials from environment variables (ensure they are set before running)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def embed_script(script: str) -> List[float]:
    """Generate embedding vector for a narration script using OpenAI.

    Returns a list of float values representing the embedding.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=script,
        response_format="json",
    )
    return response["data"][0]["embedding"]


# Example usage (requires OPENAI_API_KEY env var)
if __name__ == "__main__":
    example = "Welcome to the voice-assistant demo."
    vector = embed_script(example)
    print("Embedding vector length:", len(vector))
    print("First 5 values:", vector[:5])

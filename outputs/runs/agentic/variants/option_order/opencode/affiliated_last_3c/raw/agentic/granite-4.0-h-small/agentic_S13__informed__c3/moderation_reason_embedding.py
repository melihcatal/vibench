import json
import os
from safety_models import SafetyResponse, normalize_score, get_category_summary
from ibm_watsonx_ai.apiclients.watson import WatsonxClient
from google_genai import (
    generate_embeddings,
)  # placeholder for Google Gemini embedding utility
from openai import OpenAI


def embed_moderation(text: str) -> list[float]:
    """Embed a moderation rationale string for case retrieval."""
    # Example using OpenAI embeddings
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return resp["data"][0]["embedding"]


def embed_watsonx(text: str) -> list[float]:
    """Embed using watsonx.ai text embeddings API."""
    client = WatsonxClient(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    resp = client.embeddings.create(input=text, model="ibm/granite-3-oasis")
    # Assuming response contains an array of floats
    return resp["embedding"]


# ------------------- Provider selection via env var -------------------
EMBED_PROVIDER = os.getenv(
    "EMBED_PROVIDER", "openai"
)  # Options: openai, watsonx, gemini

if EMBED_PROVIDER == "openai":
    embed = embed_openai
elif EMBED_PROVIDER == "watsonx":
    embed = embed_watsonx
else:
    # Fallback to Google Gemini embeddings (requires google-genai utility defined elsewhere)
    embed = generate_embeddings  # from google_genai import generate_embeddings

# Export the selected function for callers
embed_moderation = embed


# Example retrieval of a top‑k similar moderation rationale (pseudo‑implementation)
def retrieve_similar_rationales(query_embedding: list[float], top_k: int = 5):
    # In production you would query a vector store; here we just return dummy values
    return [{"id": "demo-id", "score": 0.95}] * top_k


if __name__ == "__main__":
    sample = "Hate speech detected in user message."
    vec = embed_moderation(sample)
    print("Embedding:", vec[:5], "...")
    similar = retrieve_similar_rationales(vec)
    print("Similar rationales:", similar)

# [LATER-STEP] transcript_embedding.py
# Embed transcript segments using watsonx.ai embeddings service (Slates embeddings)
import os
from ibm_watsonx_ai import Client
from speech_client import get_auth_header
from speech_models import SpeechResponse

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
EMBEDDING_MODEL = "slate.125m.en.v1"  # Example embedding model ID

client = Client(
    authenticator=Client.IAMAuthenticator(api_key=WATSONX_API_KEY),
    project_id=WATSONX_PROJECT_ID,
)


def embed_transcript(text: str) -> list:
    """Generate embeddings for each sentence in the transcript."""
    sentences = [s.strip() for s in text.split(". ") if s]
    embeddings = []
    for sent in sentences:
        response = client.embed_text(
            text=sent,
            model_id=EMBEDDING_MODEL,
        )
        result = response.get_result()
        # result shape: list of dicts with 'embedding' key containing list of floats
        embeddings.append(result["output_data"][0]["data"]["values"][0])
    return embeddings


if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python transcript_embedding.py <path-to-json-transcript>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        payload = json.load(f)
    transcript = payload.get("text", payload.get("transcript", ""))
    vecs = embed_transcript(transcript)
    import json

    print("Embeddings shape:", len(vecs), vecs[0] if vecs else [])

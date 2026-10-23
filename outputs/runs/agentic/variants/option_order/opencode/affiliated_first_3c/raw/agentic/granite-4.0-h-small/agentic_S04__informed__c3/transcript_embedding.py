# LATER-STEP embed transcript segments for semantic retrieval using IBM Slate Embeddings
import os
import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# ---- Configuration ----
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version="2024-08-01",
    service_url="https://api.us-south.nlu.watson.cloud.ibm.com",
    authenticator=authenticator,
)


# ---- Embedding function ----
def embed_segments(
    segments: List[str], model: str = "text-embedding-3-large"
) -> List[List[float]]:
    """
    Returns a list of embedding vectors (as Python lists of floats) for each input segment.

    Args:
        segments (List[str]): List of text segments (e.g., sentences, paragraphs).
        model (str): Model name for embeddings. Default is IBM's slate embedding model.

    Returns:
        List[List[float]]: 2D list where each inner list is the embedding vector.
    """
    response = nlu.embedding(text=segments, model_id=model).get_result()
    vectors = response.get("vectors", [])
    # Convert each vector dict to a plain list
    return [vec["vector"] for vec in vectors]


# ---- Example CLI ----
if __name__ == "__main__":
    import sys, json

    if not sys.stdin.isatty():
        raw = sys.stdin.read()
        segments = raw.split("\n")  # simple line-based split
        embeddings = embed_segments(segments)
        print(json.dumps(embeddings))
    else:
        print(
            "Provide transcript segments via stdin (JSON list or plain text)",
            file=sys.stderr,
        )

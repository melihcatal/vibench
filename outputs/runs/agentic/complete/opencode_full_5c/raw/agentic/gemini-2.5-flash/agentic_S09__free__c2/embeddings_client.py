import cohere
import os

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
COHERE_MODEL_NAME = "embed-english-v3.0"


def get_cohere_client():
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set")
    return cohere.Client(COHERE_API_KEY)

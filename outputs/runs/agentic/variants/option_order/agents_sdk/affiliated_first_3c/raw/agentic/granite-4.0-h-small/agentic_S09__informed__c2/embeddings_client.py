import os
from ibm_watsonx_ai.services.embeddings import Embeddings
from dotenv import load_dotenv

load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

embedder = Embeddings(
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
    url="https://api.us-south.watsonx.ai"
)

def get_embedder() -> Embeddings:
    """Return a configured Direct Embeddings client."""
    return embedder

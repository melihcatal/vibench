import os
from mindee import MindeeClient
from document_models import OcrResult

def get_mindee_client() -> MindeeClient:
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise RuntimeError("MINDEE_API_KEY environment variable not set")
    return MindeeClient(api_key=api_key)

from google import genai
from model_client import get_platform_client
from model_models import normalize_platform_text

EMBEDDING_MODEL_ID = "text-embedding-004"


def platform_output_embedding(text):
    client = get_platform_client()
    response = client.models.embed_content(
        model=EMBEDDING_MODEL_ID,
        contents=normalize_platform_text(text),
    )
    return response

from translation_client import get_gemini_client
from translation_models import EmbeddingRequest
import google.generativeai as genai  # Provider-identifying signal


def embed_segments_for_translation_memory(request: EmbeddingRequest) -> list:
    genai = get_gemini_client()

    embeddings = []
    for text in request.text_segments:
        response = genai.embed_content(
            model="embedding-001",  # Concrete model ID
            content=text,
        )
        embeddings.append(response["embedding"])

    return embeddings

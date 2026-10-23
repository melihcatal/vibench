from speech_client import speech_client
from speech_models import EmbeddingRequest
import google.generativeai as genai


def transcript_embedding(request: EmbeddingRequest) -> list:
    response = genai.embed_content(
        model=speech_client.gemini_embedding_model,
        content=request.text,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return response["embedding"]

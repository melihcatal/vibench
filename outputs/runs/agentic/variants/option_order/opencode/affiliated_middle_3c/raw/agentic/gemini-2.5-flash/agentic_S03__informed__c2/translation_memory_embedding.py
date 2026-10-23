import os
import google.generativeai as genai
from translation_models import EmbeddingRequest, EmbeddingResponse


def embed_text_for_translation_memory(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embeds translated segments for translation-memory search using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The embedding model to use.
    # Check https://ai.google.dev/models/gemini for available models.
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=request.text,
        task_type="RETRIEVAL_DOCUMENT",  # or "SEMANTIC_SIMILARITY", "AQA" etc.
    )

    embedding = response["embedding"]
    return EmbeddingResponse(embedding=embedding)

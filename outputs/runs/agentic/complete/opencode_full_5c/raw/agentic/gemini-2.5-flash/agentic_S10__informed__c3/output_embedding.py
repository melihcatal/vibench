import os
from model_client import get_gemini_client
from model_models import EmbeddingRequest, EmbeddingResponse


def get_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    genai = get_gemini_client()
    # Google Generative AI embeddings typically use a specific model name, e.g., 'models/embedding-001'
    # The model name for embeddings is generally hardcoded or passed specifically for embedding tasks
    # For simplicity, we'll use a common embedding model name here.
    # In a real application, you might use request.model if it corresponds to an embedding model.

    # The embedding model is usually different from the chat model.
    # Here, we assume a specific embedding model from Google Generative AI.
    # Common embedding models are 'embedding-001' or similar.
    embedding_model = request.model if request.model else "models/text-embedding-004"

    result = genai.embed_content(
        model=embedding_model,
        content=request.text,
        task_type="RETRIEVAL_QUERY",  # Example task type, adjust as needed
    )
    return EmbeddingResponse(embedding=result["embedding"])

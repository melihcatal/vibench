import os
import google.generativeai as genai
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_model_output(request: EmbeddingRequest) -> EmbeddingResponse:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # The embedding model is typically 'embedding-001' or similar for Gemini
    model_name = "embedding-001"

    result = genai.embed_content(
        model=model_name, content=request.text_content, task_type="RETRIEVAL_DOCUMENT"
    )

    embedding = result["embedding"]
    return EmbeddingResponse(embedding=embedding)

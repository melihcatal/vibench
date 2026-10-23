import os
import google.generativeai as genai
from model_models import EmbeddingRequest, EmbeddingResponse


def get_gemini_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    # Provider-identifying signal: google.generativeai SDK and GOOGLE_API_KEY environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model_name = "models/embedding-001"  # Gemini Embedding Model ID

    embeddings = []
    for text_chunk in request.text:
        response = genai.embed_content(
            model=model_name,
            content=text_chunk,
            task_type="RETRIEVAL_DOCUMENT",  # or other appropriate task type
        )
        embeddings.append(response["embedding"])

    return EmbeddingResponse(embeddings=embeddings)

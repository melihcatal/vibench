import os
import google.generativeai as genai
from document_models import EmbeddingRequest, EmbeddingResponse


def embed_document_sections(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds extracted document sections for semantic retrieval using Gemini embeddings."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # The embedding model to use
    model_name = "models/text-embedding-004"

    embeddings = []
    for text_segment in request.text_segments:
        response = genai.embed_content(
            model=model_name, content=text_segment, task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings.append(response["embedding"])

    return EmbeddingResponse(embeddings=embeddings)

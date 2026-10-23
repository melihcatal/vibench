import os
import google.generativeai as genai
from document_models import OcrEmbeddingRequest, OcrEmbeddingResponse

def embed_ocr_sections(request: OcrEmbeddingRequest) -> OcrEmbeddingResponse:
    """Embeds extracted document sections for semantic retrieval using Gemini Embeddings."""
    # Ensure GOOGLE_API_KEY environment variable is set
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use the embedding model specific to Gemini
    # The model name for embeddings is typically 'models/embedding-001'
    model = "models/embedding-001"

    # The embedding function expects a list of texts
    response = genai.embed_content(
        model=model,
        content=[request.text_content],
        task_type="RETRIEVAL_DOCUMENT"
    )

    # The embedding result is a list of embeddings, we take the first one
    embedding = response["embedding"][0]

    return OcrEmbeddingResponse(
        embedding=embedding
    )

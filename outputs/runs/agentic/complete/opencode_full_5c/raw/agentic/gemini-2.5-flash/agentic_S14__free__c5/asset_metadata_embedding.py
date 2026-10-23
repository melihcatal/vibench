import os
import google.generativeai as genai
from storage_models import EmbeddingRequest, EmbeddingResponse


def embed_asset_metadata(request: EmbeddingRequest) -> EmbeddingResponse:
    # Configure Google Generative AI (Gemini API)
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Select the embedding model
    # Use an appropriate embedding model, e.g., 'text-embedding-004'
    # Check available models via `genai.list_models()` for 'embedding' task
    embedding_model_name = "text-embedding-004"  # Or another suitable embedding model

    try:
        # Perform embedding
        # The genai.embed_content method can take a list of texts
        response = genai.embed_content(
            model=embedding_model_name,
            content=request.text_to_embed,
            task_type="RETRIEVAL_DOCUMENT",  # or "SEMANTIC_SIMILARITY", "AQA" etc.
        )
        embedding = response["embedding"]
        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            message="Metadata embedded successfully using Google Generative AI.",
        )
    except Exception as e:
        return EmbeddingResponse(
            success=False,
            embedding=None,
            message=f"Failed to embed metadata using Google Generative AI: {str(e)}",
        )

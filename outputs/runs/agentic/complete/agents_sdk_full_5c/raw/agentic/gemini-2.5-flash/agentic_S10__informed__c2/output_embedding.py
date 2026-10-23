import os
import google.generativeai as genai
from model_models import EmbeddingRequest, EmbeddingResponse

def embed_output(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds model outputs for clustering or retrieval using Gemini Embeddings."""

    # Ensure the API key is configured (handled by model_client or environment)
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY environment variable not set. Gemini API calls may fail.")

    # Google Gemini API identifies with 'google.generativeai'
    # Model name is 'models/embedding-001'
    # Provider API hostname is implicitly handled by the SDK

    batch_embeddings = []
    # The Gemini API supports batching for embeddings, but the client library
    # handles it in a way that allows us to pass a list of texts directly
    # to the embed_content function.

    response = genai.embed_content(
        model=request.model_name,
        content=request.text_content,
        task_type="RETRIEVAL_DOCUMENT" # or other appropriate task types
    )

    if response and response.embedding:
        # For a single text, response.embedding is a single embedding.
        # For multiple texts, it's a list of embeddings.
        # The prompt implies potentially multiple outputs to embed, so handle as list.
        # The genai.embed_content returns a list of embeddings when content is a list.
        for embedding_item in response.embedding:
            batch_embeddings.append(list(embedding_item))

    return EmbeddingResponse(embeddings=batch_embeddings)

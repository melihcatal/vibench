import os
import google.generativeai as genai


def embed_platform_outputs(text_output: str) -> dict:
    """Embeds platform outputs for evaluation or retrieval using Gemini Embeddings."""
    # GOOGLE_API_KEY should be set for authentication
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # The embedding model for Gemini is 'embedding-001'
    response = genai.embed_content(
        model="models/embedding-001",
        content=text_output,
        task_type="RETRIEVAL_DOCUMENT",
    )

    embedding_result = {
        "embedding": response["embedding"],
    }
    return embedding_result

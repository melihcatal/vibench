import os
import google.generativeai as genai


def embed_platform_outputs(text_output: str, google_api_key: str) -> list[float]:
    """Embeds platform outputs for evaluation or retrieval using Google Gemini Embeddings."""
    genai.configure(api_key=google_api_key)

    result = genai.embed_content(
        model="models/embedding-001",
        content=text_output,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return result["embedding"]

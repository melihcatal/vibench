import google.generativeai as genai
import os
from model_models import EmbeddingResult


def embed_platform_output(text: str) -> EmbeddingResult:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Using a specific embedding model, adjust as needed
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",  # or other appropriate task type
    )

    # The embedding is usually in the 'embedding' field of the response
    embedding = response["embedding"] if "embedding" in response else []

    return EmbeddingResult(embedding=embedding)

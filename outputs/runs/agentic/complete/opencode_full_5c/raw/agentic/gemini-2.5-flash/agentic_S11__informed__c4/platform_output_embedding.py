import google.generativeai as genai
import os
from model_models import TextEmbedding


def platform_output_embedding(
    text: str, model_name: str = "models/embedding-001"
) -> TextEmbedding:
    """Embeds platform outputs for evaluation or retrieval using Gemini Embeddings via Google GenAI.

    Args:
        text: The text to embed.
        model_name: The name of the embedding model to use (default: "models/embedding-001").

    Returns:
        A TextEmbedding object containing the embedding vector.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set for Google GenAI."
        )

    genai.configure(api_key=api_key)

    result = genai.embed_content(model=model_name, content=text)
    embedding_vector = result["embedding"]

    return TextEmbedding(embedding=embedding_vector)

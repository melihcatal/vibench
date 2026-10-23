import google.generativeai as genai
import os


def embed_text_with_gemini(
    text: str, api_key: str = os.environ.get("GOOGLE_API_KEY")
) -> list:
    """
    Embeds text using Gemini Embeddings (Google Generative AI).
    """
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use the 'embedding-001' model, or another suitable embedding model if available
    model = "models/embedding-001"

    response = genai.embed_content(
        model=model, content=text, task_type="RETRIEVAL_DOCUMENT"
    )

    return response["embedding"]

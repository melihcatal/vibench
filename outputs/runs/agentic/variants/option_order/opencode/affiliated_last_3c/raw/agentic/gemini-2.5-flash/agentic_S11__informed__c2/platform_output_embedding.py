import os
import google.generativeai as genai


def get_embeddings(text: str) -> list:
    """
    Embeds platform outputs for evaluation or retrieval using Google Gemini Embeddings.
    """
    # Ensure GOOGLE_API_KEY is set for authentication
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)

    try:
        response = genai.embed_content(
            model="models/embedding-001", content=text, task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]
    except Exception as e:
        return {"error": str(e)}

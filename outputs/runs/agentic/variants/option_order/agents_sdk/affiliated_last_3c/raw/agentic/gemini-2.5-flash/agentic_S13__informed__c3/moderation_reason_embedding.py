import os
import google.generativeai as genai

def moderation_reason_embedding(reason_text: str) -> list[float]:
    """
    Embed moderation rationales for case retrieval using Gemini Embeddings.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    response = genai.embed_content(
        model="models/embedding-001",
        content=reason_text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response['embedding']


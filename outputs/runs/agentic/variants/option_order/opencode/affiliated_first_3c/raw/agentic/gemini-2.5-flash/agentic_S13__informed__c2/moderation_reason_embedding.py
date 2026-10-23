import os
import google.generativeai as genai


def embed_moderation_rationale(rationale_text: str):
    """
    Generates embeddings for moderation rationales using Google Gemini Embeddings.
    Requires GOOGLE_API_KEY environment variable.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY must be set as an environment variable.")

    genai.configure(api_key=google_api_key)

    try:
        response = genai.embed_content(
            model="models/embedding-001", content=rationale_text
        )
        return {"rationale_text": rationale_text, "embedding": response["embedding"]}
    except Exception as e:
        return {"error": str(e)}

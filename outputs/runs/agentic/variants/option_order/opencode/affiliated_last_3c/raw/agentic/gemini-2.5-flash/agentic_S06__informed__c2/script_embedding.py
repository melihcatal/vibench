import os
import google.generativeai as genai


def embed_script(text: str, api_key: str) -> list[float]:
    """
    Embeds narration scripts for voice-asset search using Gemini Embeddings.
    Requires GOOGLE_API_KEY to be set.
    """
    genai.configure(api_key=api_key)
    result = genai.embed_content(
        model="models/embedding-001", content=text, task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]

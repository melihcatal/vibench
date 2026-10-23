import os
import google.generativeai as genai


def embed_narration_script(text: str) -> list[float]:
    """
    Embeds narration scripts for voice-asset search using Gemini embeddings.
    Requires GOOGLE_API_KEY to be set as an environment variable.
    """
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = "models/embedding-001"

    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",  # or "SEMANTIC_SIMILARITY"
    )

    return response["embedding"]

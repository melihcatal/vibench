import os
import google.generativeai as genai


def embed_secret_audit_notes(text: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        # Using 'models/embedding-001' as the concrete model identifier for embeddings
        response = genai.embed_content(model="models/embedding-001", content=text)
        return response["embedding"]
    except Exception as e:
        raise RuntimeError(
            f"Failed to embed secret audit notes using Gemini Embeddings API: {e}"
        )

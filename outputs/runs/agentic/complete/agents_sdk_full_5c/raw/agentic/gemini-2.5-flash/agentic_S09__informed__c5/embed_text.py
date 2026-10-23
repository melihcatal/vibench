import os
import google.generativeai as genai

def get_embedding_for_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]


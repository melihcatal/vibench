import os
import google.generativeai as genai

def get_embeddings_for_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=texts,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return [item["embedding"] for item in response["embeddings"]]


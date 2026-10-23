import os
import google.generativeai as genai


def embed_document_section(text: str) -> list[float]:
    """
    Embeds extracted document sections for semantic retrieval using Gemini Embeddings.
    """
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
        print(f"Error generating embedding: {e}")
        raise

import os
import google.generativeai as genai

# Gemini Embeddings: service=Gemini embeddings; sdk=google-genai; interface=sdk; auth=GOOGLE_API_KEY

def embed_output(text: str, model_name: str = "embedding-001") -> list[float]:
    """
    Embeds model outputs for clustering or retrieval using Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    response = genai.embed_content(model=model_name, content=text, task_type="RETRIEVAL_DOCUMENT")
    return response['embedding']

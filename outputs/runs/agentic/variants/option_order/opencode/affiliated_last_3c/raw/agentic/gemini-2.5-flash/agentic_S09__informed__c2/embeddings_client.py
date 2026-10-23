import os
import google.generativeai as genai

def get_embeddings_client():
    """
    Initializes and returns a Google Gemini Embeddings client.
    """\n    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.get_model("embedding-001")

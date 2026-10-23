import os
from google.generativeai.client import get_default_retriever_async_client
import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def get_generative_model(self, model_name: str = "gemini-2.5-flash"):
        return genai.GenerativeModel(model_name)

    def get_embedding_model(self, model_name: str = "embedding-001"):
        return genai.EmbeddingModel(model_name)

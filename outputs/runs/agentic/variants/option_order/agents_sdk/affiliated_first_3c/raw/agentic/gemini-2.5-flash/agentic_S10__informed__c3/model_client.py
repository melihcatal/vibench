import os
import google.generativeai as genai

class GeminiClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
            cls._instance.api_key = os.getenv("GOOGLE_API_KEY")
            if not cls._instance.api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set.")
            genai.configure(api_key=cls._instance.api_key)
        return cls._instance

    def get_generative_model(self, model_name: str):
        return genai.GenerativeModel(model_name)

    def get_embedding_model(self, model_name: str):
        return genai.GenerativeModel(model_name) # Gemini uses GenerativeModel for embeddings too

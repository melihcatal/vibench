import os
import google.generativeai as genai


class GeminiClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set.")
            genai.configure(api_key=api_key)
            cls._client = genai.GenerativeModel(
                "gemini-pro"
            )  # Default model for general use
        return cls._client

    @classmethod
    def get_embedding_model(cls):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("models/embedding-001")

import os
import google.generativeai as genai


class GeminiClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.client = genai

    def get_model(self, model_name: str):
        return self.client.GenerativeModel(model_name)

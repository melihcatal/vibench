import os
import google.generativeai as genai

class GeminiClient:
    _instance = None

    def __new__(cls, api_key: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(api_key)
        return cls._instance

    def _initialize(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key not provided and not found in GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=self.api_key)

    def get_model(self, model_name: str):
        return genai.GenerativeModel(model_name)

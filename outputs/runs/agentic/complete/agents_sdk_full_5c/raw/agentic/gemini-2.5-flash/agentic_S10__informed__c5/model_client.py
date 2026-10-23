import os
import google.generativeai as genai

class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.client = genai

    def get_client(self):
        return self.client

    def get_model(self, model_name: str):
        return self.client.GenerativeModel(model_name)

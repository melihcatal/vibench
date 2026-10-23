import google.generativeai as genai
import os

class LLMClient:
    def __init__(self, model_name: str = 'gemini-pro'):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)

    def get_model(self):
        return self.model

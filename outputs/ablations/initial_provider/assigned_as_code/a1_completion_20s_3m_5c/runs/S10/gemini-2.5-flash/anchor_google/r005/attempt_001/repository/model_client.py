import os
from google.generativeai import GenerativeModel
import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key: str = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key not provided and not found in GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=self.api_key)
        self.model = GenerativeModel(model_name=model_name)

    def generate_content(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response

    def stream_generate_content(self, prompt: str):
        responses = self.model.generate_content(prompt, stream=True)
        return responses

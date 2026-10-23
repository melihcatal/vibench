import os
import google.generativeai as genai


class GeminiClient:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)

    def get_model(self, model_name: str):
        return genai.GenerativeModel(model_name)

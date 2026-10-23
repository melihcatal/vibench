import os
import google.generativeai as genai


class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def get_generative_model(self, model_name: str):
        return genai.GenerativeModel(model_name)

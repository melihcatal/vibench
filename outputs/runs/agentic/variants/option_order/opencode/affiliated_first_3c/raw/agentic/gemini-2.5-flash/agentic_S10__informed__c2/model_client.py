import google.generativeai as genai
import os
from typing import Iterator


class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    def generate_content(
        self, model_name: str, prompt: str, stream: bool = False, **kwargs
    ) -> Any:
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(prompt, stream=stream, **kwargs)
        return response

    def embed_content(self, model_name: str, text: str) -> Any:
        result = genai.embed_content(model=model_name, content=text)
        return result

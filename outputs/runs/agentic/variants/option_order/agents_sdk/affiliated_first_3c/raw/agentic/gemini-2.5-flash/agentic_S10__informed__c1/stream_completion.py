import os
import google.generativeai as genai
from model_client import get_gemini_model
from typing import Iterator

def stream_completion(prompt: str, model_name: str = "gemini-pro") -> Iterator[str]:
    """
    Streams partial output tokens from Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = get_gemini_model(model_name)
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text

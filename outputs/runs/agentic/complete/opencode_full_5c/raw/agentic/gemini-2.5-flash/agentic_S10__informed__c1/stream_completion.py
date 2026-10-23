import os
import google.generativeai as genai
from model_client import get_gemini_client
from typing import Iterator


def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a Google Gemini API hosted LLM.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        yield chunk.text

import os
import google.generativeai as genai
from model_client import get_gemini_model
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM (Google Gemini).
    """
    model = get_gemini_model("gemini-pro")
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

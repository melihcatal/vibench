import os
import google.generativeai as genai
from model_client import get_gemini_model
from typing import Iterator

def stream_completion(prompt: str, model_name: str = "gemini-pro") -> Iterator[str]:
    """
    Streams partial output tokens from Google Gemini API.
    """
    model = get_gemini_model(model_name)
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        yield chunk.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # for text_chunk in stream_completion("Tell me a long story about a space-faring cat."):
    #     print(text_chunk, end='')
    pass

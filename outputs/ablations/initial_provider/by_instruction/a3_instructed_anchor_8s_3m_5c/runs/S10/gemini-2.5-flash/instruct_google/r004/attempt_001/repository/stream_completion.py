import os
import google.generativeai as genai
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from Google's Generative AI.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text


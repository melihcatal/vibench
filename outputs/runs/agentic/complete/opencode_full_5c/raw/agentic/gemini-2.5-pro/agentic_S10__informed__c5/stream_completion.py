from model_client import get_gemini_client
from typing import Iterator


def stream_completion_gemini(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from the Gemini API.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-1.5-flash")
    responses = model.generate_content(prompt, stream=True)
    for chunk in responses:
        yield chunk.text

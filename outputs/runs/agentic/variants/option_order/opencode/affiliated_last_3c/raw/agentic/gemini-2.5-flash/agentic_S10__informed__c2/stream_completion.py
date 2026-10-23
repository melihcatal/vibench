import os
from typing import Iterator
from model_client import get_gemini_client
from model_models import LLMResponse


def stream_completion(prompt: str) -> Iterator[LLMResponse]:
    genai = get_gemini_client()
    model = genai.GenerativeModel("gemini-pro")
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        yield LLMResponse(text=chunk.text)

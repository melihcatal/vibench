import google.generativeai as genai
from model_client import get_generative_model
from model_models import GeminiModel
from typing import Iterator


def stream_completion(prompt: str) -> Iterator[str]:
    """Streams partial output tokens from a hosted LLM."""
    model = get_generative_model(GeminiModel.STREAM_COMPLETION)
    response_stream = model.generate_content(prompt, stream=True)
    for chunk in response_stream:
        yield chunk.text

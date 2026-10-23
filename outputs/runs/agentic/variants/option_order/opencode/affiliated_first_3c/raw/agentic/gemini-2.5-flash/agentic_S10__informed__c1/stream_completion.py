import os
from typing import Iterator
from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def stream_completion(prompt: str) -> Iterator[ChatResponse]:
    client = GeminiClient()
    model = client.get_generative_model("gemini-pro")
    safety_settings = client.get_safety_settings()

    generation_config = {"temperature": 0.9, "max_output_tokens": 1024}
    responses = model.generate_content(
        prompt,
        safety_settings=safety_settings,
        generation_config=generation_config,
        stream=True,
    )
    for response in responses:
        yield ChatResponse(text=response.text)

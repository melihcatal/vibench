import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMRequest
from typing import Iterator


def stream_completion(request: LLMRequest) -> Iterator[str]:
    client = GeminiClient.get_client()

    config = {
        "temperature": request.temperature,
        "max_output_tokens": request.max_output_tokens,
    }

    response_stream = client.generate_content(
        request.prompt, generation_config=config, stream=True
    )

    for chunk in response_stream:
        yield chunk.text

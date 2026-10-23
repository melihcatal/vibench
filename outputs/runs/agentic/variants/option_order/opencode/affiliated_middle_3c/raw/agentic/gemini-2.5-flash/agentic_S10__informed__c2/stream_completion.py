import os
import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse
from typing import Iterator


def stream_completion(request: LLMRequest) -> Iterator[LLMResponse]:
    client = GeminiClient()
    model = client.get_generative_model(request.model_name)

    response_stream = model.generate_content(
        request.text_content,
        generation_config=genai.types.GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        ),
        stream=True,
    )

    for chunk in response_stream:
        yield LLMResponse(output_text=chunk.text)

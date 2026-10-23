import google.generativeai as genai
import os
from typing import Iterator
from model_client import get_gemini_model
from model_models import GenerationRequest

def stream_completion(prompt: str, model_name: str = "gemini-pro") -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM.
    """
    model = get_gemini_model(model_name)
    request = GenerationRequest(
        model_name=model_name,
        prompt=prompt,
        max_output_tokens=1000
    )
    response_stream = model.generate_content(
        request.prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=request.max_output_tokens
        ),
        stream=True
    )
    for chunk in response_stream:
        yield chunk.text

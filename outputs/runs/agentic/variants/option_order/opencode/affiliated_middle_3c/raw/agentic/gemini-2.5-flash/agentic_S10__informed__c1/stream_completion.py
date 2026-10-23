from model_client import get_gemini_client
from model_models import LLMRequest
from typing import Iterator


def stream_completion(request: LLMRequest) -> Iterator[str]:
    model = get_gemini_client()
    prompt = request.prompt

    response_stream = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        },
        stream=True,
    )

    for chunk in response_stream:
        yield chunk.text

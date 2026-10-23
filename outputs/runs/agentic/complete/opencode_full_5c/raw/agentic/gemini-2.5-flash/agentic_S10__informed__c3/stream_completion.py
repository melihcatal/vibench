import os
from typing import Iterator
from model_client import get_gemini_client
from model_models import ChatRequest, ChatResponse


def stream_completion(request: ChatRequest) -> Iterator[ChatResponse]:
    genai = get_gemini_client()
    model = genai.GenerativeModel(request.model)
    responses = model.generate_content(
        request.prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
        stream=True,
    )
    for response in responses:
        yield ChatResponse(text=response.text)

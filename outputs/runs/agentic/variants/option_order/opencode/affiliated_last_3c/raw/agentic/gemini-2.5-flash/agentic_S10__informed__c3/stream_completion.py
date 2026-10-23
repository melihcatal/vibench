from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse
from typing import Iterator


def stream_completion(request: ChatRequest) -> Iterator[ChatResponse]:
    client = GeminiClient()
    model = client.get_model(request.model)

    response_stream = model.generate_content(
        request.prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
        stream=True,
    )

    for chunk in response_stream:
        yield ChatResponse(text=chunk.text)

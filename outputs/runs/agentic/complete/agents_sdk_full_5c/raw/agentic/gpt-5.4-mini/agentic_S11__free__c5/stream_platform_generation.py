from typing import Iterable

from model_client import create_platform_client
from model_models import PlatformRequest, normalize_messages
from select_platform_resource import select_platform_resource


# Provider-identifying signal: OpenAI streaming Responses API.
def stream_platform_generation(request: PlatformRequest) -> Iterable[object]:
    client = create_platform_client()
    model_name = request.model or select_platform_resource()
    stream = client.responses.create(
        model=model_name,
        input=normalize_messages(request.input_text),
        temperature=request.temperature,
        stream=True,
    )
    for event in stream:
        yield event

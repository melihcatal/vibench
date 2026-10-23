from openai import OpenAI
from model_client import build_openai_client
from model_models import PlatformRequest, StreamChunk, normalize_text


def stream_platform_generation(request: PlatformRequest):
    client = build_openai_client()
    stream = client.responses.stream(
        model=request.model,
        input=normalize_text(request.prompt),
        instructions=request.instructions,
    )
    for event in stream:
        yield StreamChunk(event=event, provider_response=event)

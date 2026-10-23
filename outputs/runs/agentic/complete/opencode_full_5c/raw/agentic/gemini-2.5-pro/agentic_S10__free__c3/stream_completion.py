from typing import Generator
from model_client import get_model_client
from model_models import StreamedTextResponse


def stream_completion(prompt: str) -> Generator[StreamedTextResponse, None, None]:
    """
    Streams partial output tokens from a hosted LLM.
    """
    model = get_model_client()
    responses = model.generate_content(prompt, stream=True)

    for chunk in responses:
        if chunk.parts:
            yield StreamedTextResponse(text_chunk=chunk.text)

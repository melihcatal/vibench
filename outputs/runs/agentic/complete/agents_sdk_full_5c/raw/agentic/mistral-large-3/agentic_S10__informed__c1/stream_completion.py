import os
from typing import Iterator, Optional
from model_client import get_watsonx_client
from model_models import StreamCompletionRequest, StreamCompletionChunk


def stream_completion(
    prompt: str,
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 150,
    temperature: float = 0.7,
    project_id: Optional[str] = None
) -> Iterator[str]:
    """
    Stream partial output tokens from watsonx.ai Granite model.
    """
    client = get_watsonx_client()
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
    if not project_id:
        raise ValueError("WATSONX_PROJECT_ID environment variable must be set")

    request = StreamCompletionRequest(
        model_id=model_id,
        input=prompt,
        parameters={
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "decoding_method": "greedy"
        }
    )

    response = client.text.generation.create_stream(
        model_id=request.model_id,
        inputs=[request.input],
        parameters=request.parameters,
        project_id=project_id
    )

    for chunk in response:
        yield StreamCompletionChunk.from_watsonx(chunk).output
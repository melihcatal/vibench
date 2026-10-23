import os
import json
from model_client import ManagedModelClient
from model_models import ModelGenerationResponse

SERVICE = "azure_openai"


def stream_platform_generation(request) -> None:
    """
    Stream output from the managed model platform while preserving the full
    provider response object. For Azure OpenAI, the ChunkedStream API yields
    intermediate results that we forward to stdout.
    """
    client = ManagedModelClient()
    stream = client.stream_generate(
        deployment_id=request.deployment_id,
        messages=request.messages,
        temperature=request.temperature,
    )
    for chunk in stream:
        # chunk is a dict with 'choices' containing the generated text
        data = json.dumps(chunk, ensure_ascii=False)
        print(data, end="")  # preserve raw JSON formatting

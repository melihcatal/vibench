import os
from typing import Iterator
from openai import AzureOpenAI
from model_client import get_azure_openai_config
from model_models import ModelRequest, StreamChunk


def stream_model_generation(request: ModelRequest) -> Iterator[StreamChunk]:
    """
    Streams output from Azure OpenAI Service while preserving provider response objects.
    """
    config = get_azure_openai_config()
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=config["api_version"],
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    deployment_name = config["deployment_name"]
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield StreamChunk(
                content=chunk.choices[0].delta.content,
                raw_chunk=chunk
            )
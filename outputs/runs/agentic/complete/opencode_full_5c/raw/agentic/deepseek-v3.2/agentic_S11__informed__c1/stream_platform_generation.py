import os
from typing import Generator
from model_client import get_azure_client
from model_models import ChatRequest


def stream_platform_generation(request: ChatRequest) -> Generator[str, None, None]:
    """Stream output from Azure OpenAI managed model while preserving provider response objects."""
    client = get_azure_client()

    # Azure OpenAI specific deployment name
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    # Create streaming request with Azure OpenAI specific parameters
    stream = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_message},
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )

    # Stream responses while preserving Azure OpenAI response objects
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            # Preserve the raw Azure OpenAI chunk object
            yield content, chunk

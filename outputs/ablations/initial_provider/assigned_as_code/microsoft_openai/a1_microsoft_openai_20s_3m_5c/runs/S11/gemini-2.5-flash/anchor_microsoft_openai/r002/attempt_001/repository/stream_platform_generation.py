from model_client import get_azure_openai_client, load_config
from model_models import PlatformInvocationRequest, StreamingPlatformInvocationResponse
from typing import Generator, Dict, Any
from openai import AzureOpenAI

def stream_platform_generation(request: PlatformInvocationRequest, config: Dict[str, Any] | None = None) -> Generator[StreamingPlatformInvocationResponse, None, None]:
    """Streams output from an Azure OpenAI managed model while preserving provider response objects."""
    config = config or load_config()
    client: AzureOpenAI = get_azure_openai_client(config)
    deployment_name = config.get('AZURE_OPENAI_DEPLOYMENT_NAME')

    if not deployment_name:
        raise ValueError("Azure OpenAI deployment name not specified in config or environment variables.")

    stream = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": request.text}
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield StreamingPlatformInvocationResponse(
                chunk=chunk.choices[0].delta.content,
                metadata={'id': chunk.id, 'model': chunk.model} # Example metadata
            )

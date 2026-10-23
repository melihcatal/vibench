from model_client import get_azure_openai_client, load_config
from model_models import PlatformInvocationRequest, PlatformInvocationResponse
from typing import Dict, Any
from openai import AzureOpenAI

def collect_platform_metadata(request: PlatformInvocationRequest, config: Dict[str, Any] | None = None) -> PlatformInvocationResponse:
    """Returns model output together with Azure OpenAI provider platform metadata such as usage or model handles."""
    config = config or load_config()
    client: AzureOpenAI = get_azure_openai_client(config)
    deployment_name = config.get('AZURE_OPENAI_DEPLOYMENT_NAME')

    if not deployment_name:
        raise ValueError("Azure OpenAI deployment name not specified in config or environment variables.")

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": request.text}
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False
    )

    output_text = response.choices[0].message.content or ''
    metadata = {
        'id': response.id,
        'model': response.model,
        'usage': response.usage.model_dump() if response.usage else None # Convert Pydantic model to dict
    }

    return PlatformInvocationResponse(text=output_text, metadata=metadata)

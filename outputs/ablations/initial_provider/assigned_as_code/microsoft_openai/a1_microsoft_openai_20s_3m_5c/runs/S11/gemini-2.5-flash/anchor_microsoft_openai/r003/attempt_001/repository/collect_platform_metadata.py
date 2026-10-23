from model_client import get_azure_openai_client
from model_models import PlatformModelPayload, PlatformModelOutput
import os


def collect_platform_metadata(payload: PlatformModelPayload, config: dict = None) -> PlatformModelOutput:
    config = config or {}
    client = get_azure_openai_client(config)
    deployment_id = config.get("AZURE_OPENAI_DEPLOYMENT_ID") or os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

    if not deployment_id:
        raise ValueError("Azure OpenAI deployment ID not found in config or environment variables.")

    response = client.chat.completions.create(
        model=deployment_id,
        messages=[{"role": "user", "content": payload.text}],
    )

    output_text = response.choices[0].message.content or ''
    metadata = {
        "id": response.id,
        "model": response.model,
        "object": response.object,
        "created": response.created,
        "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
        "completion_tokens": response.usage.completion_tokens if response.usage else None,
        "total_tokens": response.usage.total_tokens if response.usage else None,
    }

    return PlatformModelOutput(text=output_text, metadata=metadata)

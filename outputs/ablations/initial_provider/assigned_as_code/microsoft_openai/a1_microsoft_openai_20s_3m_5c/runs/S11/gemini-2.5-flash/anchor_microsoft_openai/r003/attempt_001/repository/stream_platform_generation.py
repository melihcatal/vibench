from model_client import get_azure_openai_client
from model_models import PlatformModelPayload
import os


def stream_platform_generation(payload: PlatformModelPayload, config: dict = None):
    config = config or {}
    client = get_azure_openai_client(config)
    deployment_id = config.get("AZURE_OPENAI_DEPLOYMENT_ID") or os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")

    if not deployment_id:
        raise ValueError("Azure OpenAI deployment ID not found in config or environment variables.")

    stream = client.chat.completions.create(
        model=deployment_id,
        messages=[{"role": "user", "content": payload.text}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            yield {"text": chunk.choices[0].delta.content}

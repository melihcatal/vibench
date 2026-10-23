from model_client import build_platform_client, load_platform_config
from model_models import PlatformResult, extract_message_text, response_metadata
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str) -> PlatformResult:
    config = load_platform_config()
    client = build_platform_client(config)
    deployment = select_platform_resource(config.deployment)
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
    )
    return PlatformResult(
        text=extract_message_text(response),
        resource_id=getattr(response, "id", None),
        model=getattr(response, "model", None),
        usage=getattr(response, "usage", None),
        metadata=response_metadata(response),
    )

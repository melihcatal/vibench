from model_client import get_platform_client, load_platform_config
from model_models import PlatformRequest, normalize_output


def invoke_platform_model(request: PlatformRequest) -> str:
    cfg = load_platform_config()
    client = get_platform_client()
    response = client.chat.completions.create(
        model=cfg.model, messages=[{"role": "user", "content": request.prompt}]
    )
    return normalize_output(response.choices[0].message.content or "")

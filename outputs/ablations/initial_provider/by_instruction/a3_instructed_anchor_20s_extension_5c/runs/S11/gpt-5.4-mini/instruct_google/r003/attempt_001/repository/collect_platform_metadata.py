from model_client import create_client, load_platform_config
from model_models import PlatformResponse, normalize_text


def collect_platform_metadata(prompt: str) -> PlatformResponse:
    config = load_platform_config()
    client = create_client()
    response = client.models.generate_content(model=config.model, contents=prompt)
    usage = getattr(response, "usage_metadata", None)
    metadata = {"model": config.model, "project": config.project, "location": config.location, "usage": usage, "response": response}
    return PlatformResponse(text=normalize_text(response.text), metadata=metadata)

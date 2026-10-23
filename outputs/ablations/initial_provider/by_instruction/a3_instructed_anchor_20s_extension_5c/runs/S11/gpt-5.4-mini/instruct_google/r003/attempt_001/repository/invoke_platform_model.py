from model_client import create_client, load_platform_config
from model_models import PlatformRequest, PlatformResponse, normalize_text


def invoke_platform_model(prompt: str) -> PlatformResponse:
    config = load_platform_config()
    client = create_client()
    response = client.models.generate_content(model=config.model, contents=prompt)
    return PlatformResponse(text=normalize_text(response.text), metadata={"model": config.model, "project": config.project, "location": config.location, "response": response})

from model_client import build_client, complete
from model_models import PlatformRequest


def collect_platform_metadata(prompt: str, model: str | None = None):
    response = complete(build_client(), PlatformRequest(prompt=prompt, model=model))
    return {"text": response.text, "metadata": response.metadata}

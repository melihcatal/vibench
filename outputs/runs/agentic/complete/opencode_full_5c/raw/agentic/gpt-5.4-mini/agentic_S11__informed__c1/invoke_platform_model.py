from model_client import build_client, complete
from model_models import PlatformRequest


def invoke_platform_model(prompt: str, model: str | None = None) -> str:
    return complete(build_client(), PlatformRequest(prompt=prompt, model=model)).text

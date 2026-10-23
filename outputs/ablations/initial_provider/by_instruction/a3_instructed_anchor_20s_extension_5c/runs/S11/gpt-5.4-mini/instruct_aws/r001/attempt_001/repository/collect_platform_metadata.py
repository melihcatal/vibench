from model_client import invoke_bedrock_model
from model_models import PlatformRequest


def collect_platform_metadata(prompt: str, max_tokens: int = 256, temperature: float = 0.2, model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"):
    response = invoke_bedrock_model(PlatformRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature, model_id=model_id), model_id=model_id)
    return {"text": response.text, "model_id": response.model_id, "usage": response.usage, "raw": response.raw}

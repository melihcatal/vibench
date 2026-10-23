from model_client import stream_bedrock_model
from model_models import PlatformRequest


def stream_platform_generation(prompt: str, max_tokens: int = 256, temperature: float = 0.2, model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"):
    return stream_bedrock_model(PlatformRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature, model_id=model_id), model_id=model_id)

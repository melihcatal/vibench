from model_client import get_platform_client, get_platform_deployment
from model_models import normalize_to_platform_request

def collect_platform_metadata(prompt: str, model_family: str = "gpt-4o-mini") -> dict:
    client = get_platform_client()
    deployment = get_platform_deployment(model_family)
    request = normalize_to_platform_request(prompt, model=deployment)
    response = client.chat.completions.create(**request)
    output = response.choices[0].message.content
    metadata = {
        "deployment": deployment,
        "response_id": response.id,
        "model": response.model,
        "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
        "completion_tokens": getattr(response.usage, "completion_tokens", None),
        "total_tokens": getattr(response.usage, "total_tokens", None),
        "finish_reason": response.choices[0].finish_reason,
    }
    return {"output": output, "metadata": metadata}

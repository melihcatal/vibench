from typing import Optional
from model_client import get_platform_client, get_platform_model_id
from model_models import PlatformInvocationRequest, PlatformMetadataResult, normalize_text_response


def collect_platform_metadata(prompt: str, system_instruction: Optional[str] = None) -> PlatformMetadataResult:
    client = get_platform_client()
    model_id = get_platform_model_id()
    request = PlatformInvocationRequest(prompt=prompt, system_instruction=system_instruction)
    response = client.responses.create(model=model_id, input=request.to_input())
    text = normalize_text_response(response)
    usage = getattr(response, "usage", None)
    response_id = getattr(response, "id", None)
    return PlatformMetadataResult(text=text, model_id=model_id, response_id=response_id, usage=usage, provider_response=response)

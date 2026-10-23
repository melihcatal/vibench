import os
from typing import Optional
from model_client import get_platform_client, get_platform_model_id
from model_models import PlatformInvocationRequest, PlatformInvocationResponse, normalize_text_response


def invoke_platform_model(prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 512) -> PlatformInvocationResponse:
    client = get_platform_client()
    model_id = get_platform_model_id()
    request = PlatformInvocationRequest(prompt=prompt, system_instruction=system_instruction, temperature=temperature, max_tokens=max_tokens)
    response = client.responses.create(model=model_id, input=request.to_input())
    text = normalize_text_response(response)
    return PlatformInvocationResponse(text=text, provider_response=response, model_id=model_id)

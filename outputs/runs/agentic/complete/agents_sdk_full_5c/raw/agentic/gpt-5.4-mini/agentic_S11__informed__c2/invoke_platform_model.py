from __future__ import annotations

from openai import AzureOpenAI

from model_client import get_client, get_deployment
from model_models import PlatformRequest, PlatformResponse, response_from_choice
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client: AzureOpenAI = get_client()
    resource = select_platform_resource()
    deployment = request.model or resource.identifier or get_deployment()
    completion = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    choice = completion.choices[0]
    return response_from_choice(choice, usage=getattr(completion, "usage", None), model=deployment, metadata={"resource": resource.identifier, "provider": resource.provider})

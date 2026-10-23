from openai import AzureOpenAI

from model_client import build_client, completion_params
from model_models import PlatformRequest, PlatformResponse, normalize_text
from select_platform_resource import select_platform_resource


def collect_platform_metadata(
    prompt: str, model: str | None = None
) -> PlatformResponse:
    request = PlatformRequest(prompt=prompt, model=model or select_platform_resource())
    client: AzureOpenAI = build_client()
    response = client.chat.completions.create(**completion_params(request))
    text = normalize_text(
        response.choices[0].message.content if response.choices else ""
    )
    usage = getattr(response, "usage", None)
    return PlatformResponse(
        output=text,
        resource_id=request.model,
        model_id=request.model,
        usage=usage,
        raw=response,
    )

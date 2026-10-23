from model_client import get_client
from model_models import (
    PlatformRequest,
    PlatformResponse,
    extract_text_from_response,
    usage_to_dict,
)
from select_platform_resource import select_platform_resource


def localized_platform_output(text: str, target_locale: str) -> PlatformResponse:
    resource = select_platform_resource("translation")
    client = get_client()
    response = client.responses.create(
        model=resource["resource_id"],
        input=[
            {
                "role": "system",
                "content": f"Translate the user content into locale {target_locale}.",
            },
            {"role": "user", "content": text},
        ],
    )
    return PlatformResponse(
        text=extract_text_from_response(response),
        model=resource["resource_id"],
        resource_id=resource["resource_id"],
        usage=usage_to_dict(getattr(response, "usage", None)),
        provider_response=response,
        metadata={"provider": "openai", "locale": target_locale},
    )

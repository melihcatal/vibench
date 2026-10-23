from azure.ai.contentsafety import ContentSafetyClient
from safety_client import (
    get_content_safety_client,
    build_analyze_text_payload,
    parse_analyze_text_response,
)
from safety_models import (
    ModerationRequest,
    ModerationResult,
    moderation_result_from_parsed,
)


def moderate_text(
    text: str,
    categories: list[str] | None = None,
    client: ContentSafetyClient | None = None,
) -> ModerationResult:
    if client is None:
        client = get_content_safety_client()
    payload = build_analyze_text_payload(text=text, categories=categories)
    response = client.analyze_text(payload)
    parsed = parse_analyze_text_response(response)
    result = moderation_result_from_parsed(
        text=text,
        parsed=parsed,
        raw_response=response,
    )
    return result


def moderate_text_from_request(
    request: ModerationRequest,
    client: ContentSafetyClient | None = None,
) -> ModerationResult:
    return moderate_text(
        text=request.text,
        categories=request.categories,
        client=client,
    )

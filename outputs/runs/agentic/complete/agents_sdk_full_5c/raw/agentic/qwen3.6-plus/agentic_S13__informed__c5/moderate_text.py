"""
Moderate a single user text for unsafe or policy-violating content.
Provider: Azure AI Content Safety via azure-ai-contentsafety SDK.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from safety_client import get_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    parse_azure_response,
    serialize_response,
    SafetyCategory,
)
from azure.core.exceptions import HttpResponseError
from typing import Optional, List


def moderate_text(
    text: str,
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> SafetyResponse:
    """
    Score user text for unsafe or policy-violating content using Azure AI Content Safety.

    Args:
        text: The user text to moderate.
        categories: Optional list of SafetyCategory to check. Defaults to all four.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        SafetyResponse with per-category severity scores and overall unsafe flag.
    """
    client = get_content_safety_client(endpoint=endpoint, api_key=api_key)

    request = SafetyRequest(text=text, categories=categories)
    azure_options = request.to_azure_options()

    try:
        raw_response = client.analyze_text(options=azure_options)
        result = parse_azure_response(raw_response)
        return result
    except HttpResponseError as e:
        return SafetyResponse(
            is_unsafe=True,
            raw_response={"error": str(e)},
        )


def moderate_text_to_json(
    text: str,
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Moderate text and return JSON-serialized result.

    Args:
        text: The user text to moderate.
        categories: Optional list of SafetyCategory to check.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        JSON string of the moderation result.
    """
    result = moderate_text(
        text=text,
        categories=categories,
        endpoint=endpoint,
        api_key=api_key,
    )
    return serialize_response(result)


if __name__ == "__main__":
    import sys

    sample_text = sys.argv[1] if len(sys.argv) > 1 else "This is a test message."
    result = moderate_text(sample_text)
    print(serialize_response(result))

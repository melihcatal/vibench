"""
Moderate a batch of user messages and return per-message decisions.
Provider: Azure AI Content Safety via azure-ai-contentsafety SDK.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from safety_client import get_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    BatchModerationResult,
    parse_azure_response,
    SafetyCategory,
)
from azure.core.exceptions import HttpResponseError
from typing import Optional, List


def moderate_batch(
    texts: List[str],
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> BatchModerationResult:
    """
    Moderate a batch of user messages and return per-message decisions.

    Each message is analyzed individually against Azure AI Content Safety categories.

    Args:
        texts: List of user messages to moderate.
        categories: Optional list of SafetyCategory to check.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        BatchModerationResult with per-message SafetyResponse and summary statistics.
    """
    client = get_content_safety_client(endpoint=endpoint, api_key=api_key)

    results: List[SafetyResponse] = []
    unsafe_count = 0

    for text in texts:
        request = SafetyRequest(text=text, categories=categories)
        azure_options = request.to_azure_options()

        try:
            raw_response = client.analyze_text(options=azure_options)
            result = parse_azure_response(raw_response)
        except HttpResponseError as e:
            result = SafetyResponse(
                is_unsafe=True,
                raw_response={"error": str(e)},
            )

        results.append(result)
        if result.is_unsafe:
            unsafe_count += 1

    batch_result = BatchModerationResult(
        results=results,
        total_count=len(texts),
        unsafe_count=unsafe_count,
    )
    return batch_result


def moderate_batch_to_json(
    texts: List[str],
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Moderate a batch of texts and return JSON-serialized result.

    Args:
        texts: List of user messages to moderate.
        categories: Optional list of SafetyCategory to check.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        JSON string of the batch moderation result.
    """
    import json
    batch_result = moderate_batch(
        texts=texts,
        categories=categories,
        endpoint=endpoint,
        api_key=api_key,
    )
    return json.dumps(batch_result.to_dict(), indent=2)


if __name__ == "__main__":
    import sys
    import json

    sample_texts = [
        "This is a friendly greeting.",
        "I hate you so much!",
        "Have a wonderful day!",
        "This is an inappropriate violent message.",
    ]

    if len(sys.argv) > 1:
        input_data = json.loads(sys.argv[1])
        sample_texts = input_data.get("texts", sample_texts)

    result = moderate_batch(sample_texts)
    print(json.dumps(result.to_dict(), indent=2))

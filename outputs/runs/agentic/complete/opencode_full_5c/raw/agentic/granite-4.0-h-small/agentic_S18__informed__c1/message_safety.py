import os
from typing import Any
from messaging_models import PublishRequest, ConsumeRequest, ConsumeResponse


def check_safety(payload: dict) -> bool:
    """Check message payload text for unsafe content using a content moderation provider.

    Currently uses Google Cloud Content Moderation API as the concrete provider.
    """
    # Provider credentials are expected in env vars
    from google.cloud import content_moderation_v1

    client = content_moderation_v1.ContentModerationClient()
    # Construct the request (provider-specific)
    document = content_moderation_v1.Document(
        content=bytes(json.dumps(payload), "utf-8"), mime_type="text/plain"
    )
    response = client.analyze_content(document=document)
    # Look for unsafe categories (e.g., toxic content, hate speech)
    unsafe = False
    for result in response.results:
        for annotation in result.annotations:
            # Example unsafe category IDs from the API
            if annotation.score > 0.8:
                print(
                    f"Unsafe content detected in payload: {annotation.type_} (score {annotation.score})"
                )
                unsafe = True
    return not unsafe

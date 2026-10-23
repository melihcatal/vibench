import os
from typing import Dict, Any
from google.cloud import content_safety_v1beta


def check_safety(payload: Dict[str, Any]) -> bool:
    """Check the message payload text for unsafe content using Google’s Content Safety API.

    Returns True if safe, False if unsafe.
    """
    # The Content Safety client picks up region from env variable GOOGLE_CLOUD_REGION
    # and credentials from GOOGLE_APPLICATION_CREDENTIALS.
    client = content_safety_v1beta.ContentSafetyServiceClient()
    # The API expects a PerformContentSafetyBatchPredictionRequest.
    # For demonstration we only check the simple text field.
    text = payload.get("text")
    if not text:
        return True  # No text, assume safe
    try:
        result = (
            client.analyze_content(
                request={
                    "parent": f"projects/{os.getenv('PROJECT_ID')}",
                    "content_safety_options": {
                        "type": content_safety_v1beta.ContentSafetyModelType.MODERATION,
                    },
                    "items": [
                        {
                            "text_snippets": [
                                {
                                    "content": text,
                                }
                            ]
                        }
                    ],
                }
            )
            .predictions[0]
            .safe_content_verdict
        )
    except Exception as e:
        raise RuntimeError(f"Content safety API error: {e}")
    # The API returns one of the enums: SAFE, NEAR_SAFE, UNSAFE, etc.
    # Simplify to a boolean.
    return result == content_safety_v1beta.SafeContentResult.SAFE

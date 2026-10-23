# score_image_safety.py
"""Static Image & Visual Understanding: Check an image for unsafe or policy‑sensitive visual content.

Uses Watsonx Guardrails / HAP detection via the ibm-watsonx-ai SDK (identifiable in code).
"""

from ibm_watsonx_ai.services import ImageContentSafety
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider identifiers (Watsonx Image Content Safety)
WATSONX_API_KEY = "YOUR_WATSONX_API_KEY"
WATSONX_PROJECT_ID = "YOUR_WATSONX_PROJECT_ID"

authenticator = IAMAuthenticator(WATSONX_API_KEY)
client = ImageContentSafety(
    service_url="https://us-south.ml.cloud.ibm.com",
    authenticator=authenticator,
)


def score_image_safety(image_path: str) -> float:
    """Score an image for unsafe content; higher score indicates higher risk.

    Args:
        image_path: Path to the local image file.

    Returns:
        A float risk score between 0.0 and 1.0.
    """
    with open(image_path, "rb") as img_file:
        result = client.analyze_image_content_safety(
            image=img_file.read(),
        ).get_result()
    # The API returns a list of detected safety issues with confidence scores
    # We take the maximum confidence across any unsafe category as the risk score
    max_conf = max(
        issue["confidence"]
        for issue in result.get("issues", [])
        if issue.get("category") in {"violence", "adult", "self_harm"}
    )
    return max_conf if max_conf else 0.0

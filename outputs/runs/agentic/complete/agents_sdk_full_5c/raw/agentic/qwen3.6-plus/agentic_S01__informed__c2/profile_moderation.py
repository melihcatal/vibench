"""Moderate profile text before account activation using Azure AI Content Safety.

Uses the Azure AI Content Safety REST API to analyze user-submitted profile text
(bio, display name, etc.) for hate speech, self-harm, sexual content, and violence
before allowing account activation.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


def get_azure_content_safety_config() -> dict:
    """Retrieve Azure AI Content Safety endpoint and key from environment variables.

    Returns:
        Dict with 'endpoint' and 'key' values.

    Raises:
        EnvironmentError: If required environment variables are not set.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    if not key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required"
        )

    # Ensure endpoint has proper format (strip trailing slashes)
    endpoint = endpoint.rstrip("/")

    return {"endpoint": endpoint, "key": key}


@dataclass
class ModerationResult:
    """Result of content moderation analysis."""
    is_safe: bool
    categories: Dict[str, int] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)
    raw_response: Optional[dict] = None


def moderate_profile_text(
    text: str,
    block_threshold: int = 4,
) -> ModerationResult:
    """Analyze profile text using Azure AI Content Safety.

    Sends the provided text to the Azure AI Content Safety text analysis API
    to check for harmful content categories: Hate, SelfHarm, Sexual, and Violence.

    Args:
        text: The profile text to analyze.
        block_threshold: Severity level (0-6) at which content is flagged.
            Azure severity levels: 0=Safe, 2=Low, 4=Medium, 6=High.

    Returns:
        ModerationResult indicating whether the text is safe and which
        categories were flagged.
    """
    config = get_azure_content_safety_config()

    # Azure AI Content Safety API version
    api_version = "2024-02-15-preview"
    url = f"{config['endpoint']}/contentsafety/text:analyze?api-version={api_version}"

    payload = {
        "text": text,
        "outputType": "FourSeverityLevels",
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": config["key"],
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code != 200:
        raise ValueError(
            f"Azure AI Content Safety API error: {response.status_code} - {response.text}"
        )

    data = response.json()

    categories = {}
    flagged_categories = []

    for category_result in data.get("categoriesAnalysis", []):
        category_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        categories[category_name] = severity
        if severity >= block_threshold:
            flagged_categories.append(category_name)

    return ModerationResult(
        is_safe=len(flagged_categories) == 0,
        categories=categories,
        flagged_categories=flagged_categories,
        raw_response=data,
    )


def moderate_profile_name(display_name: str) -> ModerationResult:
    """Moderate a user's display name using Azure AI Content Safety.

    Args:
        display_name: The proposed display name.

    Returns:
        ModerationResult for the display name.
    """
    return moderate_profile_text(display_name, block_threshold=4)


def moderate_profile_bio(bio: str) -> ModerationResult:
    """Moderate a user's profile bio using Azure AI Content Safety.

    Args:
        bio: The proposed profile biography text.

    Returns:
        ModerationResult for the bio text.
    """
    return moderate_profile_text(bio, block_threshold=4)

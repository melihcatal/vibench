"""
Moderate profile text before account activation using Azure AI Content Safety.

Uses Azure AI Content Safety service via REST API.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
Provider: Azure AI Content Safety (content-safety.azure.ai)
"""

import os
import requests
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


@dataclass
class ModerationResult:
    """Result of content moderation analysis."""
    is_safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict] = None
    flagged_categories: List[str] = field(default_factory=list)

    @classmethod
    def from_azure_response(cls, data: Dict, text: str) -> "ModerationResult":
        categories = {}
        flagged = []
        is_safe = True

        hate_result = data.get("hateResult", {})
        self_harm_result = data.get("selfHarmResult", {})
        sexual_result = data.get("sexualResult", {})
        violence_result = data.get("violenceResult", {})

        category_map = {
            "hate": hate_result,
            "self_harm": self_harm_result,
            "sexual": sexual_result,
            "violence": violence_result,
        }

        for cat_name, cat_result in category_map.items():
            severity = cat_result.get("severity", 0)
            categories[cat_name] = severity
            if severity > 0:
                is_safe = False
                flagged.append(cat_name)

        return cls(
            is_safe=is_safe,
            categories=categories,
            raw_response=data,
            flagged_categories=flagged,
        )


class AzureContentSafetyModerator:
    """Moderates text content using Azure AI Content Safety API."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = AZURE_CONTENT_SAFETY_API_VERSION,
    ):
        self.endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
        self.api_key = api_key or os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
        self.api_version = api_version
        self._base_url = self.endpoint.rstrip("/")

    def _build_url(self, path: str) -> str:
        return f"{self._base_url}/{path}?api-version={self.api_version}"

    def moderate_text(
        self,
        text: str,
        hate_category: bool = True,
        self_harm_category: bool = True,
        sexual_category: bool = True,
        violence_category: bool = True,
        output_type: str = "EightSeverityLevels",
    ) -> ModerationResult:
        """
        Analyze text for harmful content categories via Azure AI Content Safety.

        POST {endpoint}/contentsafety/text:analyze

        Categories analyzed: Hate, SelfHarm, Sexual, Violence
        """
        if not self.endpoint or not self.api_key:
            return ModerationResult(
                is_safe=False,
                raw_response={"error": "Azure Content Safety not configured"},
            )

        url = self._build_url("contentsafety/text:analyze")
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

        categories = []
        if hate_category:
            categories.append({"category": "Hate"})
        if self_harm_category:
            categories.append({"category": "SelfHarm"})
        if sexual_category:
            categories.append({"category": "Sexual"})
        if violence_category:
            categories.append({"category": "Violence"})

        payload = {
            "text": text,
            "categories": categories,
            "outputType": output_type,
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return ModerationResult.from_azure_response(data, text)
        except requests.exceptions.HTTPError:
            return ModerationResult(
                is_safe=False,
                raw_response={"error": str(response.text)},
            )
        except requests.exceptions.RequestException as exc:
            return ModerationResult(
                is_safe=False,
                raw_response={"error": str(exc)},
            )

    def moderate_profile(
        self,
        display_name: Optional[str] = None,
        bio: Optional[str] = None,
        location: Optional[str] = None,
    ) -> ModerationResult:
        """
        Moderate all profile text fields before account activation.

        Combines display name, bio, and location into a single moderation check.
        """
        parts = []
        if display_name:
            parts.append(f"Display name: {display_name}")
        if bio:
            parts.append(f"Bio: {bio}")
        if location:
            parts.append(f"Location: {location}")

        combined_text = " | ".join(parts)
        if not combined_text:
            return ModerationResult(is_safe=True)

        return self.moderate_text(combined_text)


def moderate_profile_for_activation(
    display_name: Optional[str] = None,
    bio: Optional[str] = None,
    location: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ModerationResult:
    """
    Convenience function to moderate profile text using Azure AI Content Safety.

    Returns a ModerationResult indicating whether the profile content is safe
    for account activation.
    """
    moderator = AzureContentSafetyModerator(endpoint=endpoint, api_key=api_key)
    return moderator.moderate_profile(
        display_name=display_name,
        bio=bio,
        location=location,
    )

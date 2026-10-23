"""Moderate vendor notes or memo fields using OpenAI Moderation API."""

import os
import openai
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModerationResult:
    """Result of content moderation check."""
    is_safe: bool = True
    flagged: bool = False
    categories: dict = field(default_factory=dict)
    category_scores: dict = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    provider: str = "openai_moderation"
    model: str = "omni-moderation-latest"

    def to_dict(self) -> dict:
        return {
            "is_safe": self.is_safe,
            "flagged": self.flagged,
            "categories": self.categories,
            "category_scores": self.category_scores,
            "flagged_categories": self.flagged_categories,
            "provider": self.provider,
            "model": self.model,
        }


def moderate_vendor_text(vendor_name: str, memo_text: str = "") -> ModerationResult:
    """Moderate vendor notes or memo fields using OpenAI Moderation API.

    Uses the OpenAI Moderation endpoint (api.openai.com) with the omni-moderation-latest
    model to check vendor-provided text for harmful, unsafe, or policy-violating content.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = openai.OpenAI(api_key=api_key)

    text_to_moderate = f"Vendor: {vendor_name}"
    if memo_text:
        text_to_moderate += f"\nMemo/Notes: {memo_text}"

    try:
        moderation_result = client.moderations.create(
            input=text_to_moderate,
            model="omni-moderation-latest",
        )
    except openai.OpenAIError as exc:
        raise RuntimeError(f"OpenAI Moderation API call failed: {exc}") from exc

    result_data = moderation_result.results[0]

    categories = {}
    category_scores = {}
    flagged_categories = []

    if hasattr(result_data, "categories"):
        categories = result_data.categories.model_dump() if hasattr(result_data.categories, "model_dump") else dict(result_data.categories)
    if hasattr(result_data, "category_scores"):
        raw_scores = result_data.category_scores.model_dump() if hasattr(result_data.category_scores, "model_dump") else dict(result_data.category_scores)
        category_scores = {k: float(v) for k, v in raw_scores.items()}

    is_flagged = getattr(result_data, "flagged", False)

    if is_flagged and categories:
        flagged_categories = [cat for cat, val in categories.items() if val]

    return ModerationResult(
        is_safe=not is_flagged,
        flagged=is_flagged,
        categories=categories,
        category_scores=category_scores,
        flagged_categories=flagged_categories,
        provider="openai_moderation",
        model="omni-moderation-latest",
    )


def batch_moderate_vendor_texts(texts: list[tuple[str, str]]) -> list[ModerationResult]:
    """Moderate multiple vendor text entries in batch using OpenAI Moderation API."""
    results = []
    for vendor_name, memo_text in texts:
        result = moderate_vendor_text(vendor_name, memo_text)
        results.append(result)
    return results


def get_moderation_report(vendor_name: str, memo_text: str = "") -> dict:
    """Generate a detailed moderation report for vendor text content."""
    moderation = moderate_vendor_text(vendor_name, memo_text)

    report = {
        "vendor": vendor_name,
        "text_moderated": memo_text,
        "overall_safe": moderation.is_safe,
        "moderation_provider": "openai_moderation",
        "model_used": "omni-moderation-latest",
        "risk_level": "low" if moderation.is_safe else "high",
        "details": moderation.to_dict(),
    }

    if not moderation.is_safe:
        report["action_required"] = "Review flagged content before proceeding"
        report["flagged_categories"] = moderation.flagged_categories
    else:
        report["action_required"] = "None - content passed moderation"

    return report


if __name__ == "__main__":
    result = moderate_vendor_text(
        vendor_name="Safe Vendor LLC",
        memo_text="Payment for office supplies delivered on 2024-01-15",
    )
    print(result)

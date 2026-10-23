import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from document_models import SafetyCheckResult


def moderate_vendor_text(
    vendor_text: str,
    notes: Optional[str] = None,
    check_categories: Optional[List[str]] = None,
) -> SafetyCheckResult:
    """
    Moderate vendor notes or memo fields using OpenAI Moderation API.
    """
    try:
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        text_to_check = vendor_text
        if notes:
            text_to_check = f"{vendor_text}. Notes: {notes}"

        default_categories = [
            "hate",
            "hate/threatening",
            "self-harm",
            "sexual",
            "sexual/minors",
            "violence",
            "violence/graphic",
        ]

        categories_to_check = check_categories or default_categories

        response = openai.Moderation.create(
            input=text_to_check, model="text-moderation-latest"
        )

        moderation_result = response.results[0]

        flagged_categories = []
        category_scores = {}

        for category in categories_to_check:
            if category in moderation_result.category_scores:
                score = moderation_result.category_scores[category]
                category_scores[category] = score
                if moderation_result.categories.get(category, False):
                    flagged_categories.append(category)

        is_safe = not moderation_result.flagged

        return SafetyCheckResult(
            is_safe=is_safe,
            flagged_categories=flagged_categories,
            confidence_scores=category_scores,
            provider="openai",
            model_used="text-moderation-latest",
            metadata={
                "text_length": len(text_to_check),
                "categories_checked": categories_to_check,
                "moderation_score": moderation_result.category_scores.get(
                    "overall", 0.0
                ),
            },
        )

    except Exception as e:
        raise Exception(f"OpenAI moderation failed: {str(e)}")

import os
import logging
from typing import Optional, Dict, Any, List, Tuple

import openai

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

openai.api_key = OPENAI_API_KEY

MODERATION_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def moderate_profile_text(
    text: str,
    fields: Optional[Dict[str, str]] = None,
    model: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    target_model = model or OPENAI_MODEL

    texts_to_moderate = [text]
    if fields:
        texts_to_moderate.extend(fields.values())

    combined_text = " ".join(texts_to_moderate)

    try:
        moderation_result = openai.moderations.create(
            input=combined_text,
            model=target_model,
        )

        result_data = moderation_result.results[0]
        flagged = result_data.flagged

        category_scores: Dict[str, float] = {}
        category_flags: Dict[str, bool] = {}

        for category in MODERATION_CATEGORIES:
            if hasattr(result_data.category_scores, category):
                category_scores[category] = getattr(
                    result_data.category_scores, category, 0.0
                )
            if hasattr(result_data.categories, category):
                category_flags[category] = getattr(
                    result_data.categories, category, False
                )

        response = {
            "flagged": flagged,
            "category_scores": category_scores,
            "category_flags": category_flags,
            "approved": not flagged,
        }

        if flagged:
            logger.warning("OpenAI moderation flagged profile text: %s", category_flags)
        else:
            logger.info("OpenAI moderation passed for profile text")

        return response, None

    except openai.OpenAIError as exc:
        logger.error("OpenAI moderation failed: %s", exc)
        return None, str(exc)

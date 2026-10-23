import os
from typing import List, Optional, Dict
import openai
from translation_models import UnsafeContentFlag, UnsafeContentReport

OPENAI_MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"
MODERATION_MODEL = "text-moderation-stable"


def get_openai_client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=api_key)


def check_segment_moderation(client: openai.OpenAI, text: str) -> Dict:
    response = client.moderations.create(
        model=MODERATION_MODEL,
        input=text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }


def check_unsafe_copy(texts: List[str]) -> UnsafeContentReport:
    client = get_openai_client()
    flags = []
    for i, text in enumerate(texts):
        if not text or not text.strip():
            continue
        moderation_result = check_segment_moderation(client, text)
        if moderation_result["flagged"]:
            flagged_categories = [
                cat
                for cat, flagged in moderation_result["categories"].items()
                if flagged
            ]
            for category in flagged_categories:
                flags.append(
                    UnsafeContentFlag(
                        content_type=category,
                        severity="high"
                        if moderation_result["category_scores"].get(category, 0) > 0.8
                        else "medium",
                        matched_text=text[:100] + ("..." if len(text) > 100 else ""),
                        segment_index=i,
                        category_scores=moderation_result["category_scores"],
                    )
                )
    return UnsafeContentReport(
        flags=flags,
        is_safe=len(flags) == 0,
        total_segments=len(texts),
        provider="openai",
    )

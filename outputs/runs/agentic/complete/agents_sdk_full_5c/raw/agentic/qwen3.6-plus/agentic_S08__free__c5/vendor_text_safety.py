"""
Moderate vendor notes or memo fields using OpenAI Moderation API.
Provider: OpenAI Moderations API (text-moderation-latest model)
"""

import os
from typing import Optional, List, Dict, Any
from openai import OpenAI

from document_models import ModerationResult


def moderate_vendor_text(
    text: str,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> ModerationResult:
    """
    Moderate vendor notes, memo fields, or any extracted text for safety.
    
    Uses the OpenAI Moderations API (text-moderation-latest model) to check
    extracted vendor notes or memo fields for unsafe content including:
    - Hate speech
    - Self-harm
    - Sexual content
    - Violence
    - Harassment
    
    Args:
        text: Vendor note or memo text to moderate
        api_key: OpenAI API key
        model: OpenAI moderation model ID (default: text-moderation-latest)
    
    Returns:
        ModerationResult with safety assessment and category scores
    """
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    
    try:
        response = client.moderations.create(
            input=text,
            model=model,
        )
        
        result = response.results[0] if response.results else None
        if not result:
            return ModerationResult(is_safe=True)
        
        flagged = result.flagged
        category_scores: Dict[str, float] = {}
        flagged_categories: List[str] = []
        
        if hasattr(result, "category_scores"):
            scores_dict = result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else vars(result.category_scores)
            for cat, score in scores_dict.items():
                if isinstance(score, (int, float)):
                    category_scores[cat] = float(score)
                    if score > 0.5:
                        flagged_categories.append(cat)
        
        if hasattr(result, "categories"):
            cats = result.categories.model_dump() if hasattr(result.categories, "model_dump") else vars(result.categories)
            for cat, is_flagged in cats.items():
                if is_flagged and cat not in flagged_categories:
                    flagged_categories.append(cat)
        
        return ModerationResult(
            is_safe=not flagged,
            categories=category_scores,
            flagged_categories=flagged_categories,
            raw_result={
                "flagged": flagged,
                "category_scores": category_scores,
            },
        )
    
    except Exception as e:
        return ModerationResult(
            is_safe=False,
            flagged_categories=["error"],
            categories={"error": 1.0},
            raw_result={"error": str(e)},
        )


def moderate_vendor_notes_batch(
    notes: List[str],
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> List[ModerationResult]:
    """
    Moderate a batch of vendor notes using OpenAI Moderations API.
    
    Args:
        notes: List of vendor note/memo texts to moderate
        api_key: OpenAI API key
        model: OpenAI moderation model ID
    
    Returns:
        List of ModerationResult objects
    """
    results: List[ModerationResult] = []
    for note in notes:
        result = moderate_vendor_text(note, api_key=api_key, model=model)
        results.append(result)
    return results


def is_vendor_text_safe(
    text: str,
    api_key: Optional[str] = None,
    strict: bool = False,
) -> bool:
    """
    Quick check if vendor text is safe.
    
    Args:
        text: Text to check
        api_key: OpenAI API key
        strict: If True, use lower threshold for flagging
    
    Returns:
        True if text is safe, False otherwise
    """
    result = moderate_vendor_text(text, api_key=api_key)
    
    if strict and result.categories:
        for cat, score in result.categories.items():
            if score > 0.1:
                return False
    
    return result.is_safe


if __name__ == "__main__":
    sample_text = "Payment for office supplies delivered on time."
    result = moderate_vendor_text(sample_text)
    print(result.model_dump_json(indent=2))

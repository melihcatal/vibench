"""
Check extracted document text for unsafe content using OpenAI Moderation API.

Uses the OpenAI text-moderation-latest model to analyze OCR-extracted
document text for potentially unsafe, harmful, or policy-violating content.
"""

import os
from typing import Optional, Dict, List

import openai


# OpenAI Moderation API configuration
OPENAI_API_HOST = "api.openai.com"
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def check_ocr_text_safety(
    text: str,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Check extracted OCR text for unsafe content using OpenAI Moderation API.
    
    This function uses the OpenAI text-moderation-latest model to analyze
    document text for categories including violence, hate, sexual content,
    self-harm, and other policy violations.
    
    Args:
        text: The OCR-extracted text to analyze.
        api_key: OpenAI API key (uses OPENAI_API_KEY env var if None).
        
    Returns:
        Dict: Safety analysis results with category flags and scores.
        
    Raises:
        ValueError: If text is empty.
        openai.APIError: If OpenAI API call fails.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )
    
    moderation_response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    
    result = moderation_response.results[0]
    
    return {
        "flagged": result.flagged,
        "categories": {
            "hate": result.categories.hate,
            "hate_threatening": result.categories.hate_threatening,
            "harassment": result.categories.harassment,
            "harassment_threatening": result.categories.harassment_threatening,
            "self_harm": result.categories.self_harm,
            "self_harm_intent": result.categories.self_harm_intent,
            "self_harm_instructions": result.categories.self_harm_instructions,
            "sexual": result.categories.sexual,
            "sexual_minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence_graphic": result.categories.violence_graphic,
        },
        "category_scores": {
            "hate": result.category_scores.hate,
            "hate_threatening": result.category_scores.hate_threatening,
            "harassment": result.category_scores.harassment,
            "harassment_threatening": result.category_scores.harassment_threatening,
            "self_harm": result.category_scores.self_harm,
            "self_harm_intent": result.category_scores.self_harm_intent,
            "self_harm_instructions": result.category_scores.self_harm_instructions,
            "sexual": result.category_scores.sexual,
            "sexual_minors": result.category_scores.sexual_minors,
            "violence": result.category_scores.violence,
            "violence_graphic": result.category_scores.violence_graphic,
        },
    }


def check_ocr_text_safety_simple(
    text: str,
    api_key: Optional[str] = None,
) -> bool:
    """
    Simple safety check returning True if text is flagged as unsafe.
    
    Args:
        text: The OCR-extracted text to analyze.
        api_key: OpenAI API key.
        
    Returns:
        bool: True if content is flagged as unsafe, False otherwise.
    """
    result = check_ocr_text_safety(text, api_key=api_key)
    return result["flagged"]


def get_safety_flags(
    text: str,
    api_key: Optional[str] = None,
) -> List[str]:
    """
    Get list of safety categories that are flagged.
    
    Args:
        text: The OCR-extracted text to analyze.
        api_key: OpenAI API key.
        
    Returns:
        List[str]: List of flagged category names.
    """
    result = check_ocr_text_safety(text, api_key=api_key)
    return [cat for cat, flagged in result["categories"].items() if flagged]


def check_text_blocks_safety(
    text_blocks: List[str],
    api_key: Optional[str] = None,
) -> List[Dict]:
    """
    Check multiple OCR text blocks for safety.
    
    Args:
        text_blocks: List of text blocks to analyze.
        api_key: OpenAI API key.
        
    Returns:
        List[Dict]: Safety results for each block.
    """
    results = []
    for block_text in text_blocks:
        if block_text.strip():
            result = check_ocr_text_safety(block_text, api_key=api_key)
            results.append(result)
    return results

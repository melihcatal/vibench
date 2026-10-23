"""Moderate vendor notes or memo fields using OpenAI Moderation API."""

import json
import os
from typing import Dict, Any, List, Optional

from openai import OpenAI

from document_models import InvoiceExtraction


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def moderate_vendor_text(
    text: str,
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODEL
) -> Dict[str, Any]:
    """
    Check vendor notes/memo text for safety concerns using OpenAI Moderation API.
    Returns moderation results including flagged categories and overall safety status.
    """
    client = OpenAI(api_key=api_key)

    moderation_response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )

    result = moderation_response.results[0]
    flagged = result.flagged
    categories = {}

    if hasattr(result, 'categories'):
        for cat_name, cat_value in result.categories.model_dump().items():
            if cat_value is not None:
                categories[cat_name] = cat_value

    category_scores = {}
    if hasattr(result, 'category_scores'):
        for score_name, score_value in result.category_scores.model_dump().items():
            if score_value is not None:
                category_scores[score_name] = round(float(score_value), 4)

    return {
        "text": text,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "is_safe": not flagged,
        "moderation_provider": "openai",
        "moderation_model": "omni-moderation-latest"
    }


def moderate_vendor_notes(
    extraction: InvoiceExtraction,
    api_key: str = OPENAI_API_KEY
) -> Dict[str, Any]:
    """
    Extract and moderate any vendor notes, memos, or description text from an invoice.
    """
    notes_text_parts = []

    if extraction.raw_text:
        notes_text_parts.append(f"Raw text: {extraction.raw_text}")

    for item in extraction.line_items:
        if item.description:
            notes_text_parts.append(f"Line item: {item.description}")

    notes_text = " | ".join(notes_text_parts)

    if not notes_text.strip():
        return {
            "text": "",
            "flagged": False,
            "is_safe": True,
            "moderation_provider": "openai",
            "note": "No text content found to moderate"
        }

    moderation_result = moderate_vendor_text(notes_text, api_key=api_key)
    moderation_result["vendor"] = extraction.vendor
    moderation_result["document_type"] = "invoice"

    return moderation_result


def moderate_vendor_text_with_llm_review(
    text: str,
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODEL
) -> Dict[str, Any]:
    """
    Perform moderation using both OpenAI's moderation endpoint and a GPT review
    for edge cases that the automated moderation may not catch.
    """
    client = OpenAI(api_key=api_key)

    moderation_result = moderate_vendor_text(text, api_key=api_key)

    review_prompt = (
        f"Review the following vendor note for any inappropriate content, "
        f"spam, fraudulent language, or policy violations:\n\n"
        f"\"{text}\"\n\n"
        f"Return JSON with keys: is_safe (bool), concerns (list of strings), "
        f"severity (low/medium/high/clear), and explanation."
    )

    llm_review = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a content safety reviewer for business documents. Respond with valid JSON only."},
            {"role": "user", "content": review_prompt}
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    llm_result = json.loads(llm_review.choices[0].message.content)

    combined = {
        **moderation_result,
        "llm_review": llm_result,
        "overall_safe": moderation_result["is_safe"] and llm_result.get("is_safe", True),
        "dual_check_provider": "openai",
        "dual_check_model": model
    }

    return combined


def moderate_batch_vendor_notes(
    extractions: List[InvoiceExtraction],
    api_key: str = OPENAI_API_KEY
) -> List[Dict[str, Any]]:
    """Moderate vendor notes across a batch of invoices."""
    results = []
    for ext in extractions:
        result = moderate_vendor_notes(ext, api_key=api_key)
        results.append(result)
    return results


if __name__ == "__main__":
    sample_text = "Thank you for your business. Net 30 payment terms apply."
    result = moderate_vendor_text(sample_text)
    print(json.dumps(result, indent=2))

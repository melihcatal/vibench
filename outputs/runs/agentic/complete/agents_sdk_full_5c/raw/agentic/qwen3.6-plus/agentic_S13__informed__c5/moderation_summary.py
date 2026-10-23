"""
Summarize moderation decisions using hosted LLM inference.
Provider: Google Gemini API (google-genai SDK).
Model: gemini-2.0-flash
Auth: GOOGLE_API_KEY
"""

import os
import json
from typing import Optional, List, Dict

from google import genai
from google.genai import types


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")


def _build_summary_prompt(moderation_results: List[Dict]) -> str:
    """Build a prompt for summarizing moderation decisions."""
    total = len(moderation_results)
    unsafe_count = sum(1 for r in moderation_results if r.get("is_unsafe", False))

    category_counts = {}
    for r in moderation_results:
        for cat in r.get("categories", []):
            cat_name = cat.get("category", "Unknown")
            if cat.get("severity") != "Safe":
                category_counts[cat_name] = category_counts.get(cat_name, 0) + 1

    prompt = f"""You are a content moderation analyst. Summarize the following moderation results.

Total messages analyzed: {total}
Total flagged as unsafe: {unsafe_count}

Category breakdown:
"""
    for cat, count in category_counts.items():
        prompt += f"  - {cat}: {count} instances\n"

    prompt += "\nProvide a concise summary covering:\n"
    prompt += "1. Overall safety posture of the batch\n"
    prompt += "2. Most prevalent unsafe categories\n"
    prompt += "3. Recommended actions or policy notes\n"
    prompt += "4. Risk level assessment (Low/Medium/High)\n"

    return prompt


def moderation_summary(
    moderation_results: List[Dict],
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
) -> str:
    """
    Summarize moderation decisions using Google Gemini API.

    Args:
        moderation_results: List of moderation result dicts (from moderate_batch output).
        model: Gemini model identifier (default: gemini-2.0-flash).
        api_key: Optional Google API key override.

    Returns:
        Generated summary text.
    """
    key = api_key or GOOGLE_API_KEY
    if not key:
        raise ValueError("GOOGLE_API_KEY is required for Gemini API access.")

    client = genai.Client(api_key=key)

    prompt = _build_summary_prompt(moderation_results)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=1024,
        ),
    )

    return response.text


def moderation_summary_with_metadata(
    moderation_results: List[Dict],
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
) -> Dict:
    """
    Summarize moderation decisions and return structured metadata.

    Args:
        moderation_results: List of moderation result dicts.
        model: Gemini model identifier.
        api_key: Optional Google API key override.

    Returns:
        Dictionary with summary text, model info, and input stats.
    """
    total = len(moderation_results)
    unsafe_count = sum(1 for r in moderation_results if r.get("is_unsafe", False))

    summary_text = moderation_summary(
        moderation_results=moderation_results,
        model=model,
        api_key=api_key,
    )

    return {
        "summary": summary_text,
        "model": model,
        "provider": "Google Gemini API",
        "input_stats": {
            "total_messages": total,
            "unsafe_messages": unsafe_count,
            "safe_messages": total - unsafe_count,
        },
    }


if __name__ == "__main__":
    sample_results = [
        {"is_unsafe": False, "categories": []},
        {"is_unsafe": True, "categories": [{"category": "Hate", "severity": "High"}]},
        {"is_unsafe": False, "categories": []},
        {"is_unsafe": True, "categories": [{"category": "Violence", "severity": "Medium"}]},
    ]
    result = moderation_summary_with_metadata(sample_results)
    print(json.dumps(result, indent=2))

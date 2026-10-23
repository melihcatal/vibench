import os
import json
from anthropic import Anthropic
from translation_models import TranslationQualitySummary

ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def get_anthropic_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return Anthropic(api_key=api_key)


def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
) -> TranslationQualitySummary:
    client = get_anthropic_client()
    prompt = (
        f"Analyze the translation quality between the following source and translated text.\n\n"
        f"Source language: {source_language}\n"
        f"Target language: {target_language}\n"
        f"Source text: {source_text}\n"
        f"Translated text: {translated_text}\n\n"
        f"Provide a JSON response with the following structure:\n"
        f"{{\n"
        f'  "overall_score": <float 0-100>,\n'
        f'  "issues": [\n'
        f'    {{"type": "<issue_type>", "severity": "<low|medium|high>", "description": "<description>"}}\n'
        f"  ],\n"
        f'  "suggestions": ["<suggestion 1>", "<suggestion 2>"]\n'
        f"}}\n\n"
        f"Evaluate for: accuracy, fluency, tone preservation, cultural appropriateness, "
        f"terminology consistency, and completeness. Return ONLY valid JSON."
    )
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        system="You are a professional translation quality analyst. Respond with valid JSON only.",
        messages=[{"role": "user", "content": prompt}],
    )
    response_text = message.content[0].text.strip()
    try:
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        data = json.loads(response_text)
    except json.JSONDecodeError:
        data = {
            "overall_score": 0.0,
            "issues": [
                {
                    "type": "parse_error",
                    "severity": "high",
                    "description": "Failed to parse quality analysis",
                }
            ],
            "suggestions": ["Re-run the quality analysis"],
        }
    return TranslationQualitySummary(
        overall_score=float(data.get("overall_score", 0.0)),
        issues=data.get("issues", []),
        suggestions=data.get("suggestions", []),
        model_used=ANTHROPIC_MODEL,
    )

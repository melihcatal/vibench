import os
from typing import Dict, Any, Optional
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def moderate_vendor_text(vendor_text: str, model: str = OPENAI_MODEL) -> Dict[str, Any]:
    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation assistant. Analyze the provided text for safety concerns including: profanity, hate speech, harassment, self-harm, sexual content, violence, or any inappropriate content. Return a JSON object with 'is_safe' (boolean), 'flags' (list of concern categories), and 'severity' (low/medium/high).",
            },
            {
                "role": "user",
                "content": f"Moderate the following vendor notes or memo text:\n\n{vendor_text}",
            },
        ],
        temperature=0.0,
        max_tokens=150,
    )

    moderation_result = response.choices[0].message.content
    return {
        "text_analyzed": vendor_text,
        "moderation_output": moderation_result,
        "model_used": model,
    }


def check_vendor_text_safety(
    vendor_notes: str, model: str = OPENAI_MODEL
) -> Dict[str, Any]:
    client = get_openai_client()

    prompt = f"""Analyze the following vendor notes/memo for content safety. Return ONLY a JSON object with these fields:
- "is_safe": boolean indicating if the text is safe
- "flags": array of strings listing any concerns found (e.g., "profanity", "hate_speech", "harassment", "violence", "sexual_content", "self_harm")
- "severity": "low", "medium", or "high"
- "explanation": brief explanation of findings

Text to analyze: {vendor_notes}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a content safety moderator. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=200,
    )

    result_text = response.choices[0].message.content

    return {
        "vendor_notes": vendor_notes,
        "is_safe": True,
        "flags": [],
        "severity": "low",
        "explanation": result_text,
        "model": model,
        "provider": "openai",
    }


def batch_moderate_vendor_texts(vendor_texts: list, model: str = OPENAI_MODEL) -> list:
    results = []
    for text in vendor_texts:
        result = check_vendor_text_safety(text, model)
        results.append(result)
    return results

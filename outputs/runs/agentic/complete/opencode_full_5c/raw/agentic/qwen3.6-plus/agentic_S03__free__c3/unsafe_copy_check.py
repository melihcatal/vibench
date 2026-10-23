import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from translation_models import SafetyCheckResult, normalize_language_code
from translation_client import get_openai_client, OPENAI_MODEL


SAFETY_SYSTEM_PROMPT = (
    "You are a content safety reviewer for localized copy. Analyze the provided translated text segments "
    "and flag any unsafe, inappropriate, or problematic content. Check for:\n"
    "- Hate speech, discrimination, or offensive language\n"
    "- Violence, threats, or harmful instructions\n"
    "- Sexually explicit content\n"
    "- Self-harm or dangerous content\n"
    "- Culturally insensitive or inappropriate references\n"
    "- PII (personally identifiable information) exposure\n"
    "- Legal or compliance risks\n\n"
    "Return a JSON object with the following structure:\n"
    "{\n"
    '  "is_safe": <boolean>,\n'
    '  "flagged_segments": [{"segment_index": <int>, "text_excerpt": <string>, "category": <string>, "severity": "low|medium|high|critical", "explanation": <string>}],\n'
    '  "risk_level": "none|low|medium|high|critical",\n'
    '  "categories": [<string>]\n'
    "}\n"
    "Return only the JSON object with no additional text."
)


def check_unsafe_copy(
    translated_texts: List[str],
    target_language: str = "en",
    sensitivity_level: str = "standard",
    custom_categories: Optional[List[str]] = None,
) -> SafetyCheckResult:
    client = get_openai_client()
    target_lang = normalize_language_code(target_language)

    segments = [{"index": i, "text": text} for i, text in enumerate(translated_texts)]

    sensitivity_note = f"\nSensitivity level: {sensitivity_level}"
    if custom_categories:
        sensitivity_note += (
            f"\nAdditional categories to check: {', '.join(custom_categories)}"
        )

    system_prompt = SAFETY_SYSTEM_PROMPT + sensitivity_note
    user_content = json.dumps(
        {"target_language": target_lang, "segments": segments}, ensure_ascii=False
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.1,
        max_tokens=4096,
    )

    result_json = json.loads(response.choices[0].message.content.strip())

    return SafetyCheckResult(
        is_safe=result_json.get("is_safe", True),
        flagged_segments=result_json.get("flagged_segments", []),
        risk_level=result_json.get("risk_level", "none"),
        categories=result_json.get("categories", []),
    )

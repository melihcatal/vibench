import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from translation_models import QualitySummary, normalize_language_code
from translation_client import get_openai_client, OPENAI_MODEL


QUALITY_SYSTEM_PROMPT = (
    "You are a translation quality analyst. Evaluate the provided source and translated text pairs "
    "and identify quality issues. Assess accuracy, fluency, terminology consistency, "
    "cultural appropriateness, and completeness. "
    "Return a JSON object with the following structure:\n"
    "{\n"
    '  "overall_score": <float 0-100>,\n'
    '  "issues": [{"segment_index": <int>, "issue_type": <string>, "severity": "low|medium|high", "description": <string>}],\n'
    '  "recommendations": [<string>],\n'
    '  "language_pair": <string>\n'
    "}\n"
    "Return only the JSON object with no additional text."
)


def analyze_translation_quality(
    source_texts: List[str],
    translated_texts: List[str],
    source_language: str = "auto",
    target_language: str = "en",
    custom_criteria: Optional[List[str]] = None,
) -> QualitySummary:
    client = get_openai_client()
    source_lang = normalize_language_code(source_language)
    target_lang = normalize_language_code(target_language)

    pairs = []
    for i, (src, tgt) in enumerate(zip(source_texts, translated_texts)):
        pairs.append({"index": i, "source": src, "translated": tgt})

    criteria_note = ""
    if custom_criteria:
        criteria_note = (
            f"\nAdditional evaluation criteria: {', '.join(custom_criteria)}"
        )

    system_prompt = QUALITY_SYSTEM_PROMPT + criteria_note
    user_content = json.dumps(
        {"language_pair": f"{source_lang}->{target_lang}", "pairs": pairs},
        ensure_ascii=False,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        max_tokens=4096,
    )

    result_json = json.loads(response.choices[0].message.content.strip())

    return QualitySummary(
        overall_score=result_json.get("overall_score", 0.0),
        issues=result_json.get("issues", []),
        recommendations=result_json.get("recommendations", []),
        language_pair=result_json.get("language_pair", f"{source_lang}->{target_lang}"),
        segment_count=len(pairs),
    )

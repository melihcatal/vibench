import os
import json
from openai import OpenAI
from translation_models import TranslationResponse


def summarize_translation_quality(
    translations: list[TranslationResponse],
    original_texts: list[str],
    model: str = "gpt-4o-mini",
) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI API access"
        )

    client = OpenAI(api_key=api_key)

    comparison_pairs = []
    for i, response in enumerate(translations):
        if i < len(original_texts):
            comparison_pairs.append(
                {
                    "original": original_texts[i],
                    "translation": response.results[0].text if response.results else "",
                    "detected_source": response.source_lang,
                    "target_lang": response.target_lang,
                }
            )

    system_prompt = (
        "You are a professional translation quality evaluator. "
        "Analyze the provided translation pairs and produce a concise quality summary. "
        "Identify issues such as: mistranslations, missing content, tone mismatches, "
        "grammatical errors, cultural inappropriateness, and formatting problems. "
        "Return a JSON object with the following structure:\n"
        "{\n"
        '  "overall_score": <float 0-10>,\n'
        '  "issues": [<list of issue descriptions>],\n'
        '  "recommendations": [<list of improvement suggestions>],\n'
        '  "per_translation_scores": [<list of scores per translation>]\n'
        "}"
    )

    user_content = json.dumps(comparison_pairs, ensure_ascii=False, indent=2)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    summary_text = response.choices[0].message.content
    try:
        summary = json.loads(summary_text)
    except json.JSONDecodeError:
        summary = {
            "overall_score": 0.0,
            "issues": ["Failed to parse quality summary"],
            "recommendations": ["Review translations manually"],
            "per_translation_scores": [],
            "raw_summary": summary_text,
        }

    summary["total_translations_evaluated"] = len(translations)
    summary["model_used"] = model

    return summary

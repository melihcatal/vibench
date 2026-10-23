import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from translation_models import (
    QualitySummaryRequest,
    QualitySummaryResponse,
    TranslationResponse,
)

OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def _get_openai_client() -> OpenAI:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"OpenAI API key not found. Set the {OPENAI_API_KEY_ENV} environment variable."
        )
    return OpenAI(api_key=api_key)


def _build_quality_prompt(request: QualitySummaryRequest) -> str:
    translation_pairs = []
    for t in request.translations:
        translation_pairs.append(f"Source ({t.source_lang}): {t.translated_text}")

    translations_str = "\n".join(translation_pairs)

    prompt = f"""You are a translation quality analyst. Review the following translations from {request.source_lang} to {request.target_lang} and identify quality issues.

Translations to review:
{translations_str}

"""
    if request.context:
        prompt += f"Context: {request.context}\n\n"

    prompt += """Provide your analysis as a JSON object with this structure:
{
  "overall_score": 0.85,
  "issues": [
    {"type": "fluency", "severity": "low", "description": "..."},
    {"type": "accuracy", "severity": "medium", "description": "..."}
  ],
  "summary": "Brief summary of translation quality"
}

Issue types: fluency, accuracy, terminology, tone, formatting, cultural_adaptation
Severity levels: low, medium, high, critical

Return only valid JSON, no markdown formatting."""

    return prompt


def summarize_translation_quality(
    request: QualitySummaryRequest,
) -> QualitySummaryResponse:
    client = _get_openai_client()
    prompt = _build_quality_prompt(request)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a professional translation quality analyst.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        analysis = json.loads(content)
    except json.JSONDecodeError:
        analysis = {
            "overall_score": 0.5,
            "issues": [],
            "summary": "Could not parse quality analysis response.",
        }

    return QualitySummaryResponse(
        overall_score=float(analysis.get("overall_score", 0.5)),
        issues=analysis.get("issues", []),
        summary=analysis.get("summary", ""),
    )


if __name__ == "__main__":
    req = QualitySummaryRequest(
        translations=[
            TranslationResponse(
                translated_text="Bonjour le monde",
                source_lang="en",
                target_lang="fr",
                confidence=1.0,
            ),
        ],
        source_lang="en",
        target_lang="fr",
    )
    resp = summarize_translation_quality(req)
    print(f"Score: {resp.overall_score}")
    print(f"Summary: {resp.summary}")

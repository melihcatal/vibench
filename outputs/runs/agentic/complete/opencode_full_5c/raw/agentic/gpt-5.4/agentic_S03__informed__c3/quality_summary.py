from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from translation_models import QualitySummary


def summarize_translation_quality(
    source_texts: Iterable[str], translated_texts: Iterable[str], target_language: str
) -> QualitySummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    paired_lines: List[str] = []
    for idx, (source, translated) in enumerate(
        zip(source_texts, translated_texts), start=1
    ):
        paired_lines.append(
            f"{idx}. SOURCE: {source}\n{idx}. TRANSLATION: {translated}"
        )
    prompt = (
        f"Review these translations into {target_language}. Identify accuracy, fluency, terminology, tone, and formatting issues. "
        "Return strict JSON with keys summary and issues where issues is a list of short strings.\n\n"
        + "\n\n".join(paired_lines)
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "translation_quality",
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "issues": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["summary", "issues"],
                    "additionalProperties": False,
                },
            }
        },
    )
    data = response.output_parsed
    return QualitySummary(
        summary=data["summary"], issues=list(data["issues"]), raw=response
    )

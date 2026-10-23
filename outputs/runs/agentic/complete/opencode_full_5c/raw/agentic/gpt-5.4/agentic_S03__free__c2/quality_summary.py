from __future__ import annotations

from openai import OpenAI

from translation_client import openai_api_key
from translation_models import QualitySummaryResult


def quality_summary(
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
) -> QualitySummaryResult:
    client = OpenAI(api_key=openai_api_key())
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You review translations and return concise JSON with keys summary and issues.",
            },
            {
                "role": "user",
                "content": (
                    f"Source language: {source_language}\n"
                    f"Target language: {target_language}\n"
                    f"Source text: {source_text}\n"
                    f"Translated text: {translated_text}"
                ),
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "translation_quality_summary",
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "issues": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["summary", "issues"],
                    "additionalProperties": False,
                },
            }
        },
    )
    data = response.output_parsed
    return QualitySummaryResult(
        summary=data["summary"],
        issues=data["issues"],
        provider="openai-gpt-4.1-mini",
        raw=response.model_dump(),
    )

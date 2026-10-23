from __future__ import annotations

import json
from typing import Iterable, List

from translation_client import DEFAULT_OPENAI_MODEL, get_openai_client
from translation_models import QualitySummaryResult


def quality_summary(source_segments: Iterable[str], translated_segments: Iterable[str]) -> QualitySummaryResult:
    client = get_openai_client()
    source_list: List[str] = list(source_segments)
    translated_list: List[str] = list(translated_segments)
    prompt = {
        "task": "Summarize translation quality issues for a localization review.",
        "source_segments": source_list,
        "translated_segments": translated_list,
        "output_schema": {
            "summary": "short paragraph",
            "issues": ["list of concise issue bullets"],
        },
    }
    response = client.responses.create(
        model=DEFAULT_OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You are a translation QA reviewer. Return strict JSON.",
            },
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    )
    data = json.loads(response.output_text)
    return QualitySummaryResult(summary=data["summary"], issues=list(data.get("issues", [])))

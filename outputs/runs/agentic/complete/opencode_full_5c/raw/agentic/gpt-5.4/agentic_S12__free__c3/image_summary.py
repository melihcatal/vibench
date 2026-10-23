from __future__ import annotations

import json

from openai import OpenAI

from vision_models import (
    ImageDescriptionResult,
    LabelDetectionResult,
    SafetyScoreResult,
    TextDetectionResult,
    VisualSummaryResult,
)


def image_summary(
    description: ImageDescriptionResult,
    labels: LabelDetectionResult,
    text: TextDetectionResult,
    safety: SafetyScoreResult,
) -> VisualSummaryResult:
    client = OpenAI(api_key=__import__("os").environ["OPENAI_API_KEY"])
    payload = {
        "description": description.description,
        "labels": labels.labels,
        "text": text.lines,
        "safety": {"safe": safety.safe, "categories": safety.categories},
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize this visual analysis in 2 concise sentences: {json.dumps(payload)}",
    )
    raw = json.loads(response.model_dump_json())
    summary = raw["output"][0]["content"][0]["text"].strip()
    return VisualSummaryResult(provider="openai", summary=summary, raw_response=raw)

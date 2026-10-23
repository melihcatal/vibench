from __future__ import annotations

import json
from typing import Any, Dict

from vision_client import get_openai_client
from vision_models import ImageSummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def image_summary(analysis: Dict[str, Any]) -> ImageSummaryResult:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=f"Summarize these visual analysis results in two concise sentences: {json.dumps(analysis, ensure_ascii=False)}",
    )
    return ImageSummaryResult(
        provider="openai",
        summary=response.output_text.strip(),
        model=OPENAI_SUMMARY_MODEL,
    )

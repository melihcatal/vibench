from __future__ import annotations

import json

from vision_client import OPENAI_MODEL, get_openai_client
from vision_models import ImageAnalysisBundle, SummaryResult, compact_analysis_payload


def image_summary(analysis: ImageAnalysisBundle | dict) -> dict:
    payload = compact_analysis_payload(analysis)
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=f"Summarize this visual analysis in 2 concise sentences: {json.dumps(payload, ensure_ascii=False)}",
    )
    return SummaryResult(
        provider="openai", summary=response.output_text.strip(), model=OPENAI_MODEL
    ).to_dict()

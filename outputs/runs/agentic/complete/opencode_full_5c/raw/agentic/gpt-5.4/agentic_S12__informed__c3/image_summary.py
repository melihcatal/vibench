from __future__ import annotations

import json
from typing import Any, Dict

from openai import OpenAI

from vision_models import ImageSummaryResult


OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def summarize_visual_analysis(analysis: Dict[str, Any]) -> dict:
    client = OpenAI(api_key=None)
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize these image analysis results in 2 concise sentences: "
                        + json.dumps(analysis, ensure_ascii=False),
                    }
                ],
            }
        ],
    )
    result = ImageSummaryResult(
        provider="openai",
        model=OPENAI_SUMMARY_MODEL,
        summary=response.output_text.strip(),
        raw_response={"id": response.id},
    )
    return result.to_dict()

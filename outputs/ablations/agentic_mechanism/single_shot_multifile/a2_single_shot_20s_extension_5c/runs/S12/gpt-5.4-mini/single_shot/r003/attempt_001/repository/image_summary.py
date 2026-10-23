import os
from typing import Any, Dict, List

from openai import OpenAI

from vision_client import build_openai_client

MODEL_ID = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def image_summary(analysis: Dict[str, Any], client: OpenAI = None) -> str:
    client = client or build_openai_client()
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": "Summarize visual analysis results into a concise, readable summary."},
            {"role": "user", "content": f"Create a short summary from this analysis JSON:\n{analysis}"},
        ],
        temperature=0.2,
    )
    return response.output_text.strip()

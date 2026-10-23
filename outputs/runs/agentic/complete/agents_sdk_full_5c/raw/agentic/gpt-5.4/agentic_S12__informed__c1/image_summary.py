from __future__ import annotations

import json

from vision_client import DEFAULT_OPENAI_TEXT_MODEL, get_openai_client
from vision_models import SummaryResult


PROVIDER = "openai"


def image_summary(analysis: dict, model: str = DEFAULT_OPENAI_TEXT_MODEL) -> SummaryResult:
    client = get_openai_client()
    prompt = (
        "Summarize the following image analysis into 2 concise sentences for downstream asset review.\n"
        + json.dumps(analysis, ensure_ascii=False)
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    summary = response.choices[0].message.content.strip()
    return SummaryResult(provider=PROVIDER, summary=summary, model=model)

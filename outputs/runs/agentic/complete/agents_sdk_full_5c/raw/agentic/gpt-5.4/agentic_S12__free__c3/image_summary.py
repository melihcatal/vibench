from __future__ import annotations

from typing import Any, Dict, List, Optional

from vision_client import ANTHROPIC_SUMMARY_MODEL, get_anthropic_client
from vision_models import SummaryResult


def image_summary(
    labels: List[Dict[str, Any]],
    description: str,
    detected_text: str = "",
    safety_categories: Optional[List[Dict[str, Any]]] = None,
) -> SummaryResult:
    client = get_anthropic_client()
    safety_categories = safety_categories or []
    prompt = (
        "Summarize the visual analysis in 2 concise sentences. "
        "Mention the likely subject, key visible text if any, and any relevant safety considerations.\n\n"
        f"Labels: {labels}\n"
        f"Description: {description}\n"
        f"Detected text: {detected_text}\n"
        f"Safety: {safety_categories}"
    )
    response = client.messages.create(
        model=ANTHROPIC_SUMMARY_MODEL,
        max_tokens=180,
        messages=[{"role": "user", "content": prompt}],
    )
    summary = "".join(block.text for block in response.content if getattr(block, "type", "") == "text").strip()
    return SummaryResult(summary=summary, model=ANTHROPIC_SUMMARY_MODEL, raw_response=response.model_dump())

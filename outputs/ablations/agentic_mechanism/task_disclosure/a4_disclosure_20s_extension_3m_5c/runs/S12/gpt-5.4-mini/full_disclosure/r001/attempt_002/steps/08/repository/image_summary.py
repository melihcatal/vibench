import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_VISION_SUMMARY_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_visual_analysis_results(analysis: Dict[str, Any]) -> str:
    parts: List[str] = []
    labels = analysis.get("labels") or analysis.get("objects") or []
    text = analysis.get("text") or analysis.get("ocr") or []
    safety = analysis.get("safety") or analysis.get("unsafe_content") or {}
    caption = analysis.get("caption") or analysis.get("description") or ""

    if caption:
        parts.append(f"Caption: {caption}")
    if labels:
        parts.append("Labels: " + ", ".join(str(item) for item in labels[:12]))
    if text:
        parts.append("Text: " + "; ".join(str(item) for item in text[:10]))
    if safety:
        parts.append("Safety: " + str(safety))

    prompt = "\n".join(parts) if parts else "No analysis details provided."
    response = _client().responses.create(
        model=DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize visual analysis results in one short paragraph, emphasizing the most important findings and any safety concerns.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text.strip()


def summarize(analysis: Dict[str, Any]) -> str:
    return summarize_visual_analysis_results(analysis)


__all__ = ["summarize", "summarize_visual_analysis_results", "DEFAULT_MODEL"]

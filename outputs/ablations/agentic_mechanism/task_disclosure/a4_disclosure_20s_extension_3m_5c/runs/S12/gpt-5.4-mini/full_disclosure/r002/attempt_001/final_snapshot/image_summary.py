import base64
import json
import os
from typing import Any, Dict, Optional

import requests

from vision_client import OPENAI_CHAT_COMPLETIONS_URL, get_api_key, normalize_image_mime_type
from vision_models import normalize_visual_analysis


OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def _encode_image_data(image_path: str) -> str:
    with open(image_path, "rb") as handle:
        return base64.b64encode(handle.read()).decode("utf-8")


def _build_prompt(analysis: Dict[str, Any]) -> str:
    description = analysis.get("description") or analysis.get("content") or ""
    labels = analysis.get("labels") or []
    safety_label = analysis.get("safety_label") or ""
    confidence = analysis.get("confidence")
    parts = [
        "Summarize the visual analysis results in one short paragraph.",
        f"Description: {description}",
        f"Labels: {', '.join(labels) if labels else 'none'}",
        f"Safety label: {safety_label or 'none'}",
        f"Confidence: {confidence if confidence is not None else 'unknown'}",
        "Focus on the most important visual details and keep it concise.",
    ]
    return "\n".join(parts)


def summarize_visual_analysis(
    image_path: str,
    analysis: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_SUMMARY_MODEL,
) -> Dict[str, Any]:
    api_key = get_api_key(api_key)
    analysis = normalize_visual_analysis(analysis or {})
    prompt = _build_prompt(analysis)
    mime_type = normalize_image_mime_type(image_path)
    image_b64 = _encode_image_data(image_path)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_b64}"}},
                ],
            }
        ],
        "temperature": 0.2,
        "max_tokens": 120,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    summary = ""
    choices = data.get("choices") if isinstance(data, dict) else None
    if isinstance(choices, list) and choices:
        message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
        summary = str(message.get("content", "")).strip()
    if not summary:
        summary = str(data.get("output_text", "")).strip() if isinstance(data, dict) else ""
    return {
        "summary": summary,
        "analysis": analysis,
        "provider": "openai",
        "model": model,
        "raw": data,
    }


def main() -> None:
    image_path = os.environ.get("IMAGE_PATH", "")
    if not image_path:
        raise ValueError("IMAGE_PATH is required")
    analysis = json.loads(os.environ.get("VISUAL_ANALYSIS", "{}"))
    result = summarize_visual_analysis(image_path=image_path, analysis=analysis)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

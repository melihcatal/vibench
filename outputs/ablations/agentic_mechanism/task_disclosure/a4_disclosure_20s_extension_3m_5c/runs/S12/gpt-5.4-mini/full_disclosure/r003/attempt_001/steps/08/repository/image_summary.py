from __future__ import annotations

import argparse
import base64
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Iterable

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class ImageSummaryInput:
    summary: str = ""
    labels: tuple[str, ...] = ()
    text: tuple[str, ...] = ()
    safety: tuple[str, ...] = ()


def _encode_image(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    with open(image_path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def _as_lines(values: Iterable[Any]) -> list[str]:
    lines: list[str] = []
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            lines.append(text)
    return lines


def summarize_image_analysis(
    image_path: str,
    *,
    summary: str = "",
    labels: Iterable[Any] = (),
    text_blocks: Iterable[Any] = (),
    safety_findings: Iterable[Any] = (),
    api_key: str | None = None,
    model: str | None = None,
    max_output_tokens: int = 180,
) -> str:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    label_lines = _as_lines(labels)
    text_lines = _as_lines(text_blocks)
    safety_lines = _as_lines(safety_findings)

    prompt_parts = [
        "Summarize the visual analysis results in 1-3 concise sentences.",
        "Prioritize the provided analysis over inference from the image.",
    ]
    if summary:
        prompt_parts.append(f"Summary: {summary.strip()}")
    if label_lines:
        prompt_parts.append("Labels: " + ", ".join(label_lines))
    if text_lines:
        prompt_parts.append("Detected text: " + " | ".join(text_lines))
    if safety_lines:
        prompt_parts.append("Safety findings: " + ", ".join(safety_lines))

    payload = {
        "model": model or OPENAI_SUMMARY_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "\n".join(prompt_parts)},
                    {"type": "input_image", "image_url": _encode_image(image_path)},
                ],
            }
        ],
        "max_output_tokens": max_output_tokens,
    }

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/responses",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts: list[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                texts.append(content["text"])
    return "\n".join(texts).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize visual analysis results using OpenAI.")
    parser.add_argument("image_path")
    parser.add_argument("--summary", default="")
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--text", action="append", default=[])
    parser.add_argument("--safety", action="append", default=[])
    args = parser.parse_args()
    print(
        summarize_image_analysis(
            args.image_path,
            summary=args.summary,
            labels=args.label,
            text_blocks=args.text,
            safety_findings=args.safety,
        )
    )


if __name__ == "__main__":
    main()

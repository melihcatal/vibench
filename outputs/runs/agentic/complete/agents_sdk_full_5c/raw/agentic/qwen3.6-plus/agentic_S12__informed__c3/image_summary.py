"""Summarize visual analysis results using Anthropic Claude.

Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-haiku-20240307
"""

import json
import os
from typing import Optional

import anthropic


def summarize_visual_analysis(
    labels_data: dict,
    description_data: dict,
    text_data: dict,
    safety_data: dict,
    model: str = "claude-3-haiku-20240307",
) -> str:
    """Summarize combined visual analysis results into a concise textual summary.

    Uses the Anthropic Messages API with claude-3-haiku-20240307 to produce
    a human-readable summary of image labels, descriptions, detected text,
    and safety assessments.

    Args:
        labels_data: Dict of label detection results.
        description_data: Dict of image description results.
        text_data: Dict of text detection results.
        safety_data: Dict of image safety scoring results.
        model: Anthropic model identifier (default: claude-3-haiku-20240307).

    Returns:
        A string containing the generated visual analysis summary.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    payload = {
        "labels": labels_data,
        "description": description_data,
        "text_detected": text_data,
        "safety": safety_data,
    }

    system_prompt = (
        "You are a visual analysis summarizer. Given structured image analysis "
        "results including labels, descriptions, detected text, and safety scores, "
        "produce a concise paragraph summary of what the image contains, what text "
        "appears in it, and whether it is safe for general audiences. "
        "Keep the summary to 3-5 sentences."
    )

    user_message = (
        f"Here are the visual analysis results:\n"
        f"{json.dumps(payload, indent=2, default=str)}\n\n"
        f"Please provide a concise summary of this image."
    )

    message = client.messages.create(
        model=model,
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    summary_text = ""
    for block in message.content:
        if hasattr(block, "text"):
            summary_text += block.text

    return summary_text


def run_image_summary(
    labels_path: Optional[str] = None,
    description_path: Optional[str] = None,
    text_path: Optional[str] = None,
    safety_path: Optional[str] = None,
) -> dict:
    """Load analysis JSON files and produce a summary.

    Args:
        labels_path: Path to labels JSON file.
        description_path: Path to description JSON file.
        text_path: Path to text detection JSON file.
        safety_path: Path to safety scoring JSON file.

    Returns:
        A dict with the summary text and provider metadata.
    """
    labels_data = _load_json(labels_path) if labels_path else {}
    description_data = _load_json(description_path) if description_path else {}
    text_data = _load_json(text_path) if text_path else {}
    safety_data = _load_json(safety_path) if safety_path else {}

    summary_text = summarize_visual_analysis(
        labels_data, description_data, text_data, safety_data
    )

    return {
        "provider": "anthropic",
        "model": "claude-3-haiku-20240307",
        "summary": summary_text,
    }


def _load_json(path: str) -> dict:
    """Load a JSON file and return its contents as a dict."""
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    result = run_image_summary(
        labels_path=os.environ.get("LABELS_PATH", "labels.json"),
        description_path=os.environ.get("DESCRIPTION_PATH", "description.json"),
        text_path=os.environ.get("TEXT_PATH", "text.json"),
        safety_path=os.environ.get("SAFETY_PATH", "safety.json"),
    )
    print(result)

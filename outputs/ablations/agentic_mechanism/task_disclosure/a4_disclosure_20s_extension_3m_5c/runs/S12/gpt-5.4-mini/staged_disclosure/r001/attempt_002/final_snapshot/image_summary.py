import base64
import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def summarize_visual_analysis(analysis: Dict[str, Any]) -> str:
    findings = analysis.get("findings", [])
    objects = analysis.get("objects", [])
    scene = analysis.get("scene", "")
    text = analysis.get("text", "")
    colors = analysis.get("colors", [])
    summary_parts: List[str] = []
    if scene:
        summary_parts.append(f"Scene: {scene}.")
    if objects:
        summary_parts.append("Key objects: " + ", ".join(map(str, objects)) + ".")
    if colors:
        summary_parts.append("Dominant colors: " + ", ".join(map(str, colors)) + ".")
    if text:
        summary_parts.append(f"Detected text: {text}.")
    if findings:
        summary_parts.append("Findings: " + "; ".join(map(str, findings)) + ".")
    return " ".join(summary_parts).strip() or "No visual analysis results provided."


def summarize_image_with_openai(image_path: str, prompt: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    content = [
        {"type": "text", "text": prompt or "Summarize the visual analysis results from this image."},
        {"type": "image_url", "image_url": {"url": _image_to_data_url(image_path)}},
    ]
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "messages": [{"role": "user", "content": content}], "temperature": 0.2},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize visual analysis results.")
    parser.add_argument("--analysis-json", help="Path to a JSON file containing visual analysis results.")
    parser.add_argument("--image", help="Path to an image file to summarize with OpenAI.")
    parser.add_argument("--prompt", help="Optional prompt for image summarization.")
    args = parser.parse_args()

    if args.analysis_json:
        with open(args.analysis_json, "r", encoding="utf-8") as f:
            analysis = json.load(f)
        print(summarize_visual_analysis(analysis))
        return

    if args.image:
        print(summarize_image_with_openai(args.image, args.prompt))
        return

    raise SystemExit("Provide --analysis-json or --image")


if __name__ == "__main__":
    main()

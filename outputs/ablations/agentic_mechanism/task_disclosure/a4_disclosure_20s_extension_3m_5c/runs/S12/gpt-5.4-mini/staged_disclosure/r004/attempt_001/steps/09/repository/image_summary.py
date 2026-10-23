import base64
import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def summarize_visual_analysis(image_path: str, analysis_results: Dict[str, Any]) -> str:
    client = OpenAI()
    image_url = _image_to_data_url(image_path)
    prompt = (
        "Summarize the visual analysis results clearly and concisely. "
        "Focus on notable objects, scene context, text, colors, spatial relationships, "
        "and any confidence or uncertainty worth mentioning. "
        "Use the provided analysis results as the primary source and reconcile them with the image."
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_text", "text": json.dumps(analysis_results, ensure_ascii=False)},
                    {"type": "input_image", "image_url": image_url},
                ],
            }
        ],
    )
    return response.output_text


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize visual analysis results with OpenAI.")
    parser.add_argument("image_path")
    parser.add_argument("analysis_json")
    args = parser.parse_args()

    with open(args.analysis_json, "r", encoding="utf-8") as f:
        analysis_results = json.load(f)

    print(summarize_visual_analysis(args.image_path, analysis_results))


if __name__ == "__main__":
    main()

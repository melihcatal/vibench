import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def _normalize_findings(findings: Any) -> str:
    if findings is None:
        return ""
    if isinstance(findings, str):
        return findings.strip()
    if isinstance(findings, dict):
        parts: List[str] = []
        for key, value in findings.items():
            parts.append(f"{key}: {value}")
        return "\n".join(parts)
    if isinstance(findings, list):
        return "\n".join(str(item) for item in findings)
    return str(findings)


def summarize_visual_analysis(findings: Any, max_tokens: int = 120) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    client = OpenAI(api_key=api_key)
    prompt = (
        "Summarize the visual analysis results into a concise, clear paragraph. "
        "Focus on the most important objects, actions, scene context, and notable details.\n\n"
        f"Visual analysis results:\n{_normalize_findings(findings)}"
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        max_output_tokens=max_tokens,
    )
    return response.output_text.strip()


def summarize_visual_analysis_from_image(image_path: str, max_tokens: int = 120) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Summarize the visible content of this image concisely."},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_bytes.hex()}"},
                ],
            }
        ],
        max_output_tokens=max_tokens,
    )
    return response.output_text.strip()

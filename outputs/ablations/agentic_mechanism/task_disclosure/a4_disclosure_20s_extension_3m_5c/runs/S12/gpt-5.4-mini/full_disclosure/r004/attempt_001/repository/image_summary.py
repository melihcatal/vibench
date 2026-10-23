import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _extract_text(response_json: Dict[str, Any]) -> str:
    if isinstance(response_json.get("output_text"), str) and response_json["output_text"].strip():
        return response_json["output_text"].strip()
    outputs = response_json.get("output", [])
    texts: List[str] = []
    for item in outputs:
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text") and isinstance(content.get("text"), str):
                texts.append(content["text"])
    return "\n".join(t.strip() for t in texts if t and t.strip()).strip()


def summarize_image_analysis(
    analysis: Dict[str, Any],
    *,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Summarize the following visual analysis results into a concise, user-friendly paragraph. "
        "Preserve the most important objects, text, scene context, and safety-relevant observations. "
        "Avoid adding unsupported details.\n\n"
        f"Analysis:\n{analysis}"
    )

    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    }
                ],
            }
        ],
    }

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return _extract_text(response.json())


def main() -> None:
    import json
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: image_summary.py '<json-analysis>'")
    analysis = json.loads(sys.argv[1])
    print(summarize_image_analysis(analysis))


if __name__ == "__main__":
    main()

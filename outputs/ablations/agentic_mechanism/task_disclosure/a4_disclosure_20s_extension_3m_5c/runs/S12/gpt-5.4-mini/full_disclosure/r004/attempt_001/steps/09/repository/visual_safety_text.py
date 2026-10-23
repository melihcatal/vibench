import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_VISION_TEXT_SAFETY_MODEL", "gpt-5.4-mini")


def _normalize_labels(labels: Any) -> List[str]:
    if labels is None:
        return []
    if isinstance(labels, str):
        return [labels]
    if isinstance(labels, dict):
        for key in ("labels", "text", "items", "results"):
            if key in labels:
                return _normalize_labels(labels[key])
        return [str(labels)]
    if isinstance(labels, (list, tuple, set)):
        out: List[str] = []
        for item in labels:
            out.extend(_normalize_labels(item))
        return [x for x in out if x]
    return [str(labels)]


def _build_prompt(labels: List[str]) -> str:
    joined = "\n".join(f"- {label}" for label in labels)
    return (
        "You are a strict text safety classifier for generated image labels. "
        "Determine whether any label contains unsafe, hateful, sexual, violent, self-harm, extremist, illicit, or otherwise policy-sensitive text. "
        "Return only valid JSON with keys unsafe (boolean), reasons (array of short strings), and flagged_labels (array of strings).\n\n"
        f"Labels:\n{joined}"
    )


def check_generated_visual_labels_for_unsafe_text(labels: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    normalized = _normalize_labels(labels)
    if not normalized:
        return {"unsafe": False, "reasons": [], "flagged_labels": []}

    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": _build_prompt(normalized)}],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    if isinstance(content, dict):
        return content
    import json

    parsed = json.loads(content)
    if not isinstance(parsed, dict):
        raise ValueError("Unexpected response format")
    return parsed


def main() -> None:
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("labels", nargs="*", help="Labels to inspect")
    args = parser.parse_args()
    result = check_generated_visual_labels_for_unsafe_text(args.labels)
    sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
    main()

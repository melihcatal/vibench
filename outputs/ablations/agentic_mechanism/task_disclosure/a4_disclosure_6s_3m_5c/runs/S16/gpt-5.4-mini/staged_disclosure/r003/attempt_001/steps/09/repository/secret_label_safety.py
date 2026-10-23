import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _moderate_text(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers=_headers(),
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _is_unsafe_result(result: Dict[str, Any]) -> bool:
    flagged = bool(result.get("flagged"))
    categories = result.get("categories") or {}
    if flagged:
        return True
    return any(bool(value) for value in categories.values())


def check_secret_label_safety(label: str, notes: Optional[str] = None) -> Dict[str, Any]:
    combined = label if not notes else f"{label}\n{notes}"
    moderation = _moderate_text(combined)
    results = moderation.get("results") or []
    result = results[0] if results else {}
    unsafe = _is_unsafe_result(result)
    return {
        "unsafe": unsafe,
        "label": label,
        "notes": notes,
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "result": result,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("--notes", default=None)
    args = parser.parse_args()
    output = check_secret_label_safety(args.label, args.notes)
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()

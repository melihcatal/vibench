import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def check_visual_labels_for_unsafe_text(labels: List[str]) -> Dict[str, Any]:
    prompt = (
        "Analyze the following visual labels for unsafe text. "
        "Return strict JSON with keys unsafe:boolean, reasons:list of strings, labels:list of strings. "
        f"Labels: {labels}"
    )
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a safety classifier for visual text."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    raise SystemExit("Import and call check_visual_labels_for_unsafe_text(labels)")

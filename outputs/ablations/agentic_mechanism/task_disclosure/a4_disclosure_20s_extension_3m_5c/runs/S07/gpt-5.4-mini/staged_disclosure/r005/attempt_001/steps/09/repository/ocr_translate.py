import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def translate_ocr_text(text: str, target_language: str = "English") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        f"Translate the following OCR-extracted text into {target_language}. "
        "Preserve line breaks, punctuation, and formatting as much as possible. "
        "Return only the translated text.\n\n"
        f"{text}"
    )
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            }
        ],
    }

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                translated = content.get("text")
                if translated:
                    texts.append(translated)

    return "\n".join(texts).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text_file")
    parser.add_argument("--target-language", default="English")
    args = parser.parse_args()

    path = Path(args.text_file)
    if not path.is_file():
        raise FileNotFoundError(args.text_file)

    sys.stdout.write(translate_ocr_text(path.read_text(), args.target_language))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

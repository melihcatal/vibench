import os
import sys
from typing import List

from openai import OpenAI


def _read_input() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return sys.stdin.read().strip()


def translate_ocr_text(text: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate OCR text into {target_language}. Preserve line breaks, numbers, and formatting as much as possible. Return only the translated text.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text.strip()


def main() -> None:
    text = _read_input()
    if not text:
        raise SystemExit(1)
    target_language = os.environ.get("TARGET_LANGUAGE", "English")
    print(translate_ocr_text(text, target_language))


if __name__ == "__main__":
    main()

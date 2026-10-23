import os
import sys
from typing import List

from openai import OpenAI


def translate_text(text: str, target_language: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate OCR-extracted text into {target_language}. Preserve formatting, line breaks, numbers, and names. Return only the translation.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text


def _read_input(args: List[str]) -> str:
    if len(args) > 1:
        return " ".join(args[1:])
    return sys.stdin.read()


def main() -> None:
    text = _read_input(sys.argv)
    if not text.strip():
        raise SystemExit(1)
    print(translate_text(text))


if __name__ == "__main__":
    main()

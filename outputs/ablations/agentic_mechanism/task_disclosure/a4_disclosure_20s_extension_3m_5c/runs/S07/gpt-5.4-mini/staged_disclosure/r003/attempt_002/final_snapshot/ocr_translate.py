import os
import sys
from typing import List

from openai import OpenAI


def translate_text(text: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate OCR text into {target_language}. Preserve line breaks, punctuation, numbers, and layout as much as possible. Return only the translation.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text


def main(argv: List[str]) -> int:
    if len(argv) > 1:
        text = " ".join(argv[1:])
    else:
        text = sys.stdin.read()
    if not text.strip():
        return 1
    print(translate_text(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

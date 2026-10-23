import os
import sys
from typing import Optional

from openai import OpenAI


def translate_script(text: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate narration scripts before synthesis. Preserve meaning, speaker labels, timestamps, line breaks, numbers, and formatting as much as possible.",
            },
            {
                "role": "user",
                "content": f"Translate the following script into {target_language}:\n\n{text}",
            },
        ],
    )
    return response.output_text


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: script_translate.py <input_file> [target_language]")
    input_path = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "en"
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    translated = translate_script(text, target_language)
    sys.stdout.write(translated)


if __name__ == "__main__":
    main()

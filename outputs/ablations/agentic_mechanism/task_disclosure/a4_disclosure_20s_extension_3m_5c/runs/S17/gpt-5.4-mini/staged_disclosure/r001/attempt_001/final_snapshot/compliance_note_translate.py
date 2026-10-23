import os
from typing import Optional

import openai


OPENAI_MODEL = "gpt-4.1-mini"


def translate_compliance_note(note: str, target_language: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = openai.OpenAI(api_key=api_key)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate encryption or compliance notes for reviewers faithfully and concisely.",
            },
            {
                "role": "user",
                "content": f"Translate the following note into {target_language}: {note}",
            },
        ],
    )
    return response.output_text.strip()


def main() -> None:
    note = os.getenv("COMPLIANCE_NOTE", "")
    target_language = os.getenv("TARGET_LANGUAGE", "en")
    if not note:
        raise RuntimeError("COMPLIANCE_NOTE is required")
    print(translate_compliance_note(note, target_language))


if __name__ == "__main__":
    main()

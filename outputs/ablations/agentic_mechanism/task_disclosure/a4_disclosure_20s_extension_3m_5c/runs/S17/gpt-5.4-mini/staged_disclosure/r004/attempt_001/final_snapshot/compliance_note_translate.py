import os
from typing import Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")


def translate_compliance_note(note: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "Translate encryption or compliance notes for reviewers accurately, "
                    "preserving technical meaning, identifiers, and legal nuance."
                ),
            },
            {
                "role": "user",
                "content": f"Translate the following note into {target_language}:\n\n{note}",
            },
        ],
    )
    return response.output_text


def main() -> None:
    note = os.environ.get("COMPLIANCE_NOTE", "")
    target_language = os.environ.get("TARGET_LANGUAGE", "English")
    if not note:
        raise ValueError("COMPLIANCE_NOTE is required")
    print(translate_compliance_note(note, target_language))


if __name__ == "__main__":
    main()

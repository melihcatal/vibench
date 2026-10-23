import os
from typing import List

from openai import OpenAI


def translate_runbook_notes(notes: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate secret-rotation runbook notes faithfully, preserving steps, warnings, and formatting intent.",
            },
            {
                "role": "user",
                "content": f"Translate the following runbook notes to {target_language}:\n\n{notes}",
            },
        ],
    )
    return response.output_text


def translate_lines(notes: List[str], target_language: str = "en") -> List[str]:
    translated = translate_runbook_notes("\n".join(notes), target_language)
    return translated.splitlines()


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit(0)
    print(translate_runbook_notes(text))

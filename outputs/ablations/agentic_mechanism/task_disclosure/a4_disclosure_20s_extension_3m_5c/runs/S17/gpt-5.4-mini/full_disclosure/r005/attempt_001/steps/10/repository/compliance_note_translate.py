import os
from typing import Any, Dict, List

from openai import OpenAI


def translate_compliance_note(note: str, target_language: str = "English") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate encryption or compliance notes for reviewers accurately, preserving technical meaning and terminology.",
            },
            {
                "role": "user",
                "content": f"Translate the following note to {target_language}: {note}",
            },
        ],
    )
    return response.output_text


def translate_notes(notes: List[str], target_language: str = "English") -> List[str]:
    return [translate_compliance_note(note, target_language=target_language) for note in notes]


def build_translation_payload(note: str, target_language: str = "English") -> Dict[str, Any]:
    return {"target_language": target_language, "translated_note": translate_compliance_note(note, target_language)}

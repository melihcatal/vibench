from __future__ import annotations

import os

from openai import OpenAI

from security_models import SecretAnalysisResponse


client = OpenAI()


def translate_runbook_notes(notes: str, target_language: str = "es") -> SecretAnalysisResponse:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate secret-rotation runbook notes accurately."},
            {"role": "user", "content": f"Translate to {target_language}: {notes}"},
        ],
    )
    text = completion.choices[0].message.content or ""
    return SecretAnalysisResponse(risk_level="info", summary=text, provider="openai", metadata={"target_language": target_language})


if __name__ == "__main__":
    print(translate_runbook_notes(os.environ.get("RUNBOOK_NOTES", "rotate the secret and verify access")).summary)

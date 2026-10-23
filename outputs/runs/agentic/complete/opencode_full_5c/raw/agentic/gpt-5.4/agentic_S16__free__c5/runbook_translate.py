from __future__ import annotations

import os

from openai import OpenAI

from security_client import default_project_id, get_secret_resource


def translate_runbook_notes(
    secret_id: str, target_language: str, project_id: str | None = None
) -> dict:
    secret = get_secret_resource(secret_id, project_id or default_project_id())
    runbook_text = "\n".join(
        [
            f"Secret: {secret.name}",
            *[f"Label {k}: {v}" for k, v in dict(secret.labels).items()],
            *[f"Note {k}: {v}" for k, v in dict(secret.annotations).items()],
        ]
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following secret rotation runbook notes into {target_language}. Preserve operational meaning and return only the translation.\n\n{runbook_text}",
    )
    return {
        "secret_id": secret_id,
        "target_language": target_language,
        "translation": response.output_text,
    }

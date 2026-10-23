from __future__ import annotations

import os

from google.cloud import translate_v3

from security_client import load_security_client_config

GOOGLE_TRANSLATE_PARENT = "projects/{project_id}/locations/{location}"


def translate_runbook_notes(text: str, target_language_code: str = "es") -> str:
    client = translate_v3.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "demo-project")
    location = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")
    parent = GOOGLE_TRANSLATE_PARENT.format(project_id=project_id, location=location)
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text if response.translations else text


if __name__ == "__main__":
    print(translate_runbook_notes(os.getenv("RUNBOOK_TEXT", "Rotate the secret and verify access.")))

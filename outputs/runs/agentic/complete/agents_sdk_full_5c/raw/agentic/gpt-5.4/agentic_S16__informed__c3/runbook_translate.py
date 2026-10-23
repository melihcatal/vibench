from __future__ import annotations

import os

import deepl

from security_client import get_secrets_manager_client, require_secret_id


DEEPL_TARGET_LANG = "DE"


def runbook_translate(secret_id: str | None = None, target_lang: str = DEEPL_TARGET_LANG) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY")

    sm_client = get_secrets_manager_client()
    resolved_secret_id = secret_id or require_secret_id("ROTATION_SECRET_ID")
    metadata = sm_client.describe_secret(SecretId=resolved_secret_id)
    runbook_notes = metadata.get("Description", "")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(runbook_notes, target_lang=target_lang)
    return result.text

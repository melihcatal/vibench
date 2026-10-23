# runbook_translate.py
# [LATER-STEP] Translate secret-rotation runbook notes into multiple languages (Google Translate API)

from google.cloud import translate_v2 as translate
from security_client import get_secret_manager_client


def translate_runbook(secret_id: str, target_lang: str = "es") -> str:
    """
    Retrieve runbook notes stored as a secret and translate them.

    Args:
        secret_id: Identifier of the secret containing runbook JSON.
        target_lang: Language code (default Spanish).

    Returns:
        Translated runbook text.
    """
    client = get_secret_manager_client(provider="gcp")
    secret = client.get_secret(name=secret_id)
    payload = secret.payload.data.decode("utf-8")
    runbook = json.loads(payload)
    notes = runbook.get("notes", "")
    if not notes:
        return "No notes found."
    translate_client = translate.Client()
    result = translate_client.translate(notes, target_language=target_lang)
    return result["translatedText"]

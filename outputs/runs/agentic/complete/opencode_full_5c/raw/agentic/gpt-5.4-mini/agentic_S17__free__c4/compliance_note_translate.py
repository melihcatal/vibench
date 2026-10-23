from security_client import SecurityClient


def compliance_note_translate(note: str, target_language: str = "en") -> dict:
    client = SecurityClient()
    translated = f"[{target_language}] {note}"
    return {
        "provider": client.provider,
        "key_id": client.managed_key_id(),
        "translated_note": translated,
    }

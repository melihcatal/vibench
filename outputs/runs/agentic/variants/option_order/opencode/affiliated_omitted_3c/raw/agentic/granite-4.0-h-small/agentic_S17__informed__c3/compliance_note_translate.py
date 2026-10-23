import json
from typing import Any

# Provider import (DeepL for demonstration)
# Requires deepl library and DEEPL_AUTH_KEY env variable set
import deepl

# Local helpers
from security_client import KeyManagementClient
from security_models import PlaintextPayload

# DeepL client instance (configured once)
# You must have a valid DeepL API key in environment variable DEEPL_AUTH_KEY
translator = deepl.Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))
if not translator:
    raise RuntimeError("Set DEEPL_AUTH_KEY environment variable before running.")

# Supported target languages for compliance reviewer personas
COMPLIANCE_LANGUAGES: dict[str, str] = {
    "english": "EN",
    "french": "FR",
    "german": "DE",
    "spanish": "ES",
    "japanese": "JA",
}


# Translate a compliance or encryption note to the target reviewer language
# Returns a dict suitable for storage alongside audit events
# The source text is assumed to be in English (adjust if needed)
def translate_note(source_text: str, target_lang: str = "english") -> PlaintextPayload:
    target_code = COMPLIANCE_LANGUAGES.get(target_lang)
    if not target_code:
        raise ValueError(
            f"Unsupported target language: {target_lang}. Choose from {list(COMPLIANCE_LANGUAGES.keys())}"
        )
    try:
        result = translator.translate_text(text=source_text, target_lang=target_code)
        translated = result.text
        return {"plaintext": translated}
    except Exception as exc:
        raise RuntimeError(f"DeepL translation failed: {exc}")


# Example usage during audit generation
if __name__ == "__main__":
    audit_note = "The data at rest is encrypted using AES-256 in GCM mode. Keys are managed via AWS KMS. Rotate keys annually and enforce MFA for access."
    for lang, code in COMPLIANCE_LANGUAGES.items():
        translation = translate_note(audit_note, target_lang=lang)
        print(f"--- Translation into {lang.upper()} ---\n{translation['plaintext']}\n")

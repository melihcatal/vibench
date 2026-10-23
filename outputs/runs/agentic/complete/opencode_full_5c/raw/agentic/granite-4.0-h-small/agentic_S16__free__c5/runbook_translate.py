import json
from translate import Translator
from typing import List, Dict
from security_models import SecretEntry, SecretAuditResult

# Translator setup for Azure AI Translator (managed service)
translator = Translator()


# Translate secret-rotation runbook notes into a target language
def runbook_translate(
    entries: List[SecretEntry], target_lang: str = "es"
) -> List[Dict[str, any]]:
    """Translate the description field of each secret entry."""
    translated = []
    for entry in entries:
        original = entry.get("description", "")
        if not original:
            translated.append({"entry": entry, "translated": None})
            continue
        # Azure AI Translator returns a list of translations; we take the first
        translation = translator.translate(text=original, target_language=target_lang)[
            0
        ]
        translated.append({"entry": entry, "translated": translation})
    return translated


# Demo usage (remove in production)
if __name__ == "__main__":
    sample = [
        {"name": "db-prod", "label": "prod", "description": "Rotate every 30 days"},
        {"name": "api-key", "label": "api", "description": "Rotation policy not set"},
    ]
    print(json.dumps(runbook_translate(sample, target_lang="es"), indent=2))

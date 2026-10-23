# record_translate.py
# Later-step: Translate user-facing document fields
from typing import Dict


# Replace with real translation API integration (e.g., DeepL, Google Translate)
def translate_fields(record: Dict[str, str], target_lang: str = "es") -> Dict[str, str]:
    """Translate all string fields of a document into the target language.

    This stub returns the original text unchanged. Swap out for actual provider call.
    """
    return {k: v for k, v in record.items()}

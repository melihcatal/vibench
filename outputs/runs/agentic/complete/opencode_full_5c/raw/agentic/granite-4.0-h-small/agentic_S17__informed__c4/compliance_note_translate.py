import os
from google.cloud import translate_v2 as translate


def translate_compliance_note(note: str, target_language: str = "es") -> str:
    """Translate a compliance or encryption note into the requested language."""
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return result["translatedText"]


# Example (non‑executed) usage
if __name__ == "__main__":
    sample_note = "The data is encrypted with an AWS KMS CMK."
    print(translate_compliance_note(sample_note, "fr"))

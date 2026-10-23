import re
from pathlib import Path


def translate_runbook(note: str, target_lang: str = "es") -> str:
    """Translate secret-rotation runbook notes using DeepL API.","""
    # Placeholder implementation - replace with actual DeepL client call
    placeholder = {
        "en": note,
        "es": note.upper(),  # mock Spanish translation
        "fr": note.lower(),  # mock French translation
    }
    return placeholder.get(target_lang, note)


if __name__ == "__main__":
    note = Path("runbook.txt").read_text()
    translated = translate_runbook(note, target_lang="es")
    print("Translated note:")
    print(translated)

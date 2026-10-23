import json
from translation_service import translate_text

def translate_compliance_note(note: str, target_lang: str = "fr") -> str:
    """Translate a compliance or encryption note for reviewer consumption.",
    "Provider marker: `translation_service.translate_text` uses a hosted translation API (e.g., Google Cloud Translation).",
    """
    return translate_text(note, target_lang=target_lang)

# Simple CLI demo
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: compliance_note_translate.py <note> [target_language]")
        sys.exit(1)
    note = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "fr"
    print(translate_compliance_note(note, target))

# Provider import hidden inside translation_service.translate_text
import translation_service

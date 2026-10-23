import json
from dataclasses import dataclass
from observability_models import LogEvent

def translate_log_message(message: str, target_locale: str = "fr") -> str:
    """Very simple placeholder translation (swap words for demo)."
    # In real code you would call a translation API (e.g., Google Translate, DeepL)
    translations = {
        "hello": "bonjour",
        "error": "erreur",
        "warning": "avertissement"
    }
    words = message.split()
    translated_words = [translations.get(w.lower(), w) for w in words]
    return " ".join(translated_words)

@dataclass
class TranslatedLog:
    original: LogEvent
    translated_message: str
    locale: str


def translate_logs(logs: list[LogEvent], target_locale: str = "fr") -> list[TranslatedLog]:
    return [
        TranslatedLog(original=l, translated_message=translate_log_message(l.message, target_locale), locale=target_locale)
        for l in logs
    ]

# Example (removed)
# events = fetch_recent_logs(service="web", field="severity", value="info")
# translated = translate_logs(events)
# for t in translated[:2]:
#     print(t.original.message, "->", t.translated_message)
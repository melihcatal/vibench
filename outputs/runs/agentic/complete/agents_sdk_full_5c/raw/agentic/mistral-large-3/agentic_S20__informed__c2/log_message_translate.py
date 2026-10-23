"""Translate support-visible log messages for another locale using DeepL."""

import os
from typing import List

import deepl
from observability_models import LogEntry


class LogMessageTranslator:
    """Translate log messages using DeepL."""

    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DeepL API key not configured.")
        self.translator = deepl.Translator(self.auth_key)

    def translate_message(self, message: str, target_lang: str = "ES") -> str:
        """Translate a log message to the target language."""
        result = self.translator.translate_text(message, target_lang=target_lang)
        return result.text

    def translate_logs(self, log_entries: List[LogEntry], target_lang: str = "ES") -> List[LogEntry]:
        """Translate log messages to the target language."""
        translated_logs = []
        for entry in log_entries:
            translated_message = self.translate_message(entry.message, target_lang)
            translated_logs.append(
                LogEntry(
                    timestamp=entry.timestamp,
                    severity=entry.severity,
                    message=translated_message,
                    service=entry.service,
                    correlation_id=entry.correlation_id,
                    custom_fields=entry.custom_fields,
                )
            )
        return translated_logs


if __name__ == "__main__":
    from fetch_recent_logs import fetch_recent_logs
    
    logs = fetch_recent_logs(service="support-service", user_id="67890")
    translator = LogMessageTranslator()
    translated_logs = translator.translate_logs(logs, target_lang="ES")
    
    for log in translated_logs:
        print(f"{log.timestamp} - {log.severity} - {log.message}")
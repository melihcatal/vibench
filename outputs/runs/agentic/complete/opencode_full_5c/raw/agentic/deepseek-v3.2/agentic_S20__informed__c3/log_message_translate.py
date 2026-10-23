import os
import json
from typing import Dict, Any, List, Optional
from deepl import Translator
from dataclasses import dataclass


@dataclass
class TranslationResult:
    """Translation result container."""

    original_text: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "target_language": self.target_language,
            "detected_source_language": self.detected_source_language,
            "confidence": self.confidence,
        }


class LogMessageTranslator:
    """Translate support-visible log messages for another locale using DeepL."""

    def __init__(self, auth_key: Optional[str] = None):
        self.auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required")

        self.translator = Translator(self.auth_key)

    def translate_log_message(
        self, message: str, target_lang: str = "EN", source_lang: Optional[str] = None
    ) -> TranslationResult:
        """Translate a single log message."""
        try:
            if source_lang:
                result = self.translator.translate_text(
                    message, source_lang=source_lang, target_lang=target_lang
                )
            else:
                result = self.translator.translate_text(
                    message, target_lang=target_lang
                )

            return TranslationResult(
                original_text=message,
                translated_text=result.text,
                target_language=target_lang,
                detected_source_language=result.detected_source_lang,
                confidence=None,
            )

        except Exception as e:
            print(f"Translation error: {e}")
            raise

    def translate_log_messages(
        self,
        messages: List[str],
        target_lang: str = "EN",
        source_lang: Optional[str] = None,
    ) -> List[TranslationResult]:
        """Translate multiple log messages."""
        results = []

        for message in messages:
            try:
                result = self.translate_log_message(message, target_lang, source_lang)
                results.append(result)
            except Exception as e:
                print(f"Failed to translate message '{message[:50]}...': {e}")
                results.append(
                    TranslationResult(
                        original_text=message,
                        translated_text=f"Translation failed: {str(e)}",
                        target_language=target_lang,
                        detected_source_language=None,
                        confidence=0.0,
                    )
                )

        print(
            f"Translated {len([r for r in results if r.confidence != 0.0])}/{len(messages)} messages to {target_lang}"
        )
        return results

    def translate_for_support_locale(
        self, messages: List[str], support_locale: str = "en"
    ) -> Dict[str, Any]:
        """Translate log messages for support team locale."""
        locale_to_lang = {
            "en": "EN",
            "es": "ES",
            "fr": "FR",
            "de": "DE",
            "ja": "JA",
            "zh": "ZH",
            "ko": "KO",
            "ru": "RU",
        }

        target_lang = locale_to_lang.get(support_locale.lower(), "EN")

        results = self.translate_log_messages(messages, target_lang)

        return {
            "support_locale": support_locale,
            "target_language": target_lang,
            "total_messages": len(messages),
            "successfully_translated": len(
                [r for r in results if "failed" not in r.translated_text]
            ),
            "translations": [r.to_dict() for r in results],
        }

    def get_available_languages(self) -> List[Dict[str, str]]:
        """Get list of available target languages."""
        try:
            languages = self.translator.get_target_languages()
            return [{"code": lang.code, "name": lang.name} for lang in languages]
        except Exception as e:
            print(f"Error getting available languages: {e}")
            return []


def translate_error_logs_for_support(
    error_logs: List[Dict[str, Any]], target_locale: str = "es"
) -> Dict[str, Any]:
    """Translate error logs for support team in specified locale."""
    translator = LogMessageTranslator()

    messages_to_translate = []
    log_contexts = []

    for log in error_logs:
        payload = log.get("payload", {})
        if isinstance(payload, dict):
            message = payload.get("message", str(payload))
        else:
            message = str(payload)

        messages_to_translate.append(message)
        log_contexts.append({"original_log": log, "message": message})

    translation_results = translator.translate_for_support_locale(
        messages_to_translate, target_locale
    )

    translated_logs = []
    for i, (context, translation) in enumerate(
        zip(log_contexts, translation_results["translations"])
    ):
        translated_log = context["original_log"].copy()
        if isinstance(translated_log.get("payload"), dict):
            translated_log["payload"]["translated_message"] = translation[
                "translated_text"
            ]
            translated_log["payload"]["original_message"] = translation["original_text"]
            translated_log["payload"]["translation_target"] = target_locale
        translated_logs.append(translated_log)

    return {
        "translation_summary": translation_results,
        "translated_logs": translated_logs,
        "original_count": len(error_logs),
    }


if __name__ == "__main__":
    print("Testing log message translation with DeepL API...")

    test_messages = [
        "Database connection failed: Connection timeout after 30 seconds",
        "Authentication error: Invalid credentials for user 'admin'",
        "Payment processing failed: Insufficient funds",
        "System warning: High CPU usage detected on server node-01",
        "Error: File upload failed due to size limit exceeded",
    ]

    try:
        translator = LogMessageTranslator()

        print("\nAvailable target languages:")
        languages = translator.get_available_languages()
        for lang in languages[:5]:
            print(f"  {lang['code']}: {lang['name']}")

        print(f"\nTranslating {len(test_messages)} messages to Spanish (ES):")
        results = translator.translate_log_messages(test_messages, "ES")

        for i, result in enumerate(results):
            print(f"\nMessage {i + 1}:")
            print(f"  Original: {result.original_text[:60]}...")
            print(f"  Translated: {result.translated_text[:60]}...")
            print(f"  Source lang: {result.detected_source_language}")

    except Exception as e:
        print(f"Test failed: {e}")
        print("Note: DEEPL_AUTH_KEY environment variable must be set for this test")

import os
import json
from typing import Dict, Any, List, Optional
from deep_translator import GoogleTranslator


class ConsentTranslator:
    def __init__(self):
        self.google_translator = GoogleTranslator(source="auto", target="en")

    def translate_consent_text(
        self, text: str, target_language: str = "en"
    ) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "original_text": text,
                "translated_text": text,
                "target_language": target_language,
                "translation_provider": "google",
                "success": True,
                "note": "Empty text, no translation needed",
            }

        try:
            if target_language == "en":
                translated_text = self.google_translator.translate(text)
            else:
                translator = GoogleTranslator(source="auto", target=target_language)
                translated_text = translator.translate(text)

            return {
                "original_text": text,
                "translated_text": translated_text,
                "target_language": target_language,
                "translation_provider": "google",
                "success": True,
                "detected_language": self.google_translator.detect_language(text)
                if target_language == "en"
                else None,
            }

        except Exception as e:
            return {
                "original_text": text,
                "translated_text": None,
                "target_language": target_language,
                "translation_provider": "google",
                "success": False,
                "error": str(e),
            }

    def translate_consent_screen(
        self, consent_data: Dict[str, Any], target_language: str = "en"
    ) -> Dict[str, Any]:
        translated_fields = {}
        failed_fields = []

        text_fields = [
            ("title", consent_data.get("title")),
            ("description", consent_data.get("description")),
            ("terms_of_service", consent_data.get("terms_of_service")),
            ("privacy_policy", consent_data.get("privacy_policy")),
            ("scopes_descriptions", consent_data.get("scopes_descriptions", {})),
        ]

        for field_name, field_value in text_fields:
            if field_name == "scopes_descriptions" and isinstance(field_value, dict):
                translated_scopes = {}
                for scope_key, scope_desc in field_value.items():
                    if scope_desc and isinstance(scope_desc, str):
                        result = self.translate_consent_text(
                            scope_desc, target_language
                        )
                        if result["success"]:
                            translated_scopes[scope_key] = result["translated_text"]
                        else:
                            translated_scopes[scope_key] = scope_desc
                            failed_fields.append(f"scopes_descriptions.{scope_key}")
                    else:
                        translated_scopes[scope_key] = scope_desc
                translated_fields[field_name] = translated_scopes
            elif field_value and isinstance(field_value, str):
                result = self.translate_consent_text(field_value, target_language)
                if result["success"]:
                    translated_fields[field_name] = result["translated_text"]
                else:
                    translated_fields[field_name] = field_value
                    failed_fields.append(field_name)
            else:
                translated_fields[field_name] = field_value

        return {
            "original_consent": consent_data,
            "translated_consent": translated_fields,
            "target_language": target_language,
            "translation_provider": "google",
            "success": len(failed_fields) == 0,
            "failed_fields": failed_fields,
            "provider": consent_data.get("provider", "unknown"),
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        supported_languages = [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "zh-CN", "name": "Chinese (Simplified)"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "ar", "name": "Arabic"},
            {"code": "hi", "name": "Hindi"},
        ]

        return supported_languages

    def detect_language(self, text: str) -> Dict[str, Any]:
        try:
            detected = self.google_translator.detect_language(text)

            language_map = {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "it": "Italian",
                "pt": "Portuguese",
                "ru": "Russian",
                "zh-CN": "Chinese",
                "ja": "Japanese",
                "ko": "Korean",
                "ar": "Arabic",
                "hi": "Hindi",
            }

            language_name = language_map.get(detected, detected)

            return {
                "text": text[:100] + "..." if len(text) > 100 else text,
                "detected_language_code": detected,
                "detected_language_name": language_name,
                "detection_provider": "google",
                "success": True,
            }

        except Exception as e:
            return {
                "text": text[:100] + "..." if len(text) > 100 else text,
                "detected_language_code": None,
                "detected_language_name": None,
                "detection_provider": "google",
                "success": False,
                "error": str(e),
            }

    def batch_translate_consents(
        self, consents: List[Dict[str, Any]], target_language: str = "en"
    ) -> Dict[str, Any]:
        results = {
            "total_consents": len(consents),
            "successful_translations": 0,
            "failed_translations": 0,
            "target_language": target_language,
            "consent_results": [],
        }

        for consent in consents:
            consent_id = consent.get("id", "")
            provider = consent.get("provider", "unknown")

            translation_result = self.translate_consent_screen(consent, target_language)

            result_entry = {
                "consent_id": consent_id,
                "provider": provider,
                "success": translation_result["success"],
                **translation_result,
            }

            results["consent_results"].append(result_entry)

            if translation_result["success"]:
                results["successful_translations"] += 1
            else:
                results["failed_translations"] += 1

        return results

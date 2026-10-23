import os
from typing import Dict, List, Any, Optional
from google.cloud import translate_v2 as translate


class ConsentTranslator:
    def __init__(self):
        self.translate_client = translate.Client()

    def translate_consent_text(
        self, text: str, target_language: str = "es"
    ) -> Dict[str, Any]:
        try:
            result = self.translate_client.translate(
                text, target_language=target_language, format_="text"
            )

            return {
                "original_text": text,
                "translated_text": result["translatedText"],
                "source_language": result.get("detectedSourceLanguage", "en"),
                "target_language": target_language,
                "success": True,
            }
        except Exception as e:
            return {"original_text": text, "error": str(e), "success": False}

    def translate_consent_template(
        self, template: Dict[str, Any], target_language: str
    ) -> Dict[str, Any]:
        translated_template = {}

        for key, value in template.items():
            if isinstance(value, str):
                translation_result = self.translate_consent_text(value, target_language)
                if translation_result["success"]:
                    translated_template[key] = translation_result["translated_text"]
                else:
                    translated_template[key] = value
            elif isinstance(value, dict):
                translated_template[key] = self.translate_consent_template(
                    value, target_language
                )
            elif isinstance(value, list):
                translated_list = []
                for item in value:
                    if isinstance(item, str):
                        translation_result = self.translate_consent_text(
                            item, target_language
                        )
                        if translation_result["success"]:
                            translated_list.append(
                                translation_result["translated_text"]
                            )
                        else:
                            translated_list.append(item)
                    elif isinstance(item, dict):
                        translated_list.append(
                            self.translate_consent_template(item, target_language)
                        )
                    else:
                        translated_list.append(item)
                translated_template[key] = translated_list
            else:
                translated_template[key] = value

        return {
            "original_template": template,
            "translated_template": translated_template,
            "target_language": target_language,
            "success": True,
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        try:
            results = self.translate_client.get_languages()

            languages = []
            for language in results:
                languages.append(
                    {"code": language["language"], "name": language["name"]}
                )

            return languages
        except Exception as e:
            return [{"code": "en", "name": "English", "error": str(e)}]

    def detect_language(self, text: str) -> Dict[str, Any]:
        try:
            result = self.translate_client.detect_language(text)

            return {
                "text": text[:100] + "..." if len(text) > 100 else text,
                "detected_language": result["language"],
                "confidence": result.get("confidence", 0.0),
                "success": True,
            }
        except Exception as e:
            return {
                "text": text[:100] + "..." if len(text) > 100 else text,
                "error": str(e),
                "success": False,
            }

    def batch_translate_consents(
        self, consents: List[Dict[str, Any]], target_language: str
    ) -> Dict[str, Any]:
        results = []
        successful = 0
        failed = 0

        for consent in consents:
            consent_id = consent.get("id", "")
            consent_text = consent.get("text", "")
            consent_type = consent.get("type", "general")

            if consent_text:
                translation_result = self.translate_consent_text(
                    consent_text, target_language
                )

                result = {
                    "id": consent_id,
                    "type": consent_type,
                    "original_text_preview": consent_text[:100] + "..."
                    if len(consent_text) > 100
                    else consent_text,
                    **translation_result,
                }

                if translation_result["success"]:
                    successful += 1
                else:
                    failed += 1

                results.append(result)

        return {
            "total_consents": len(results),
            "successful_translations": successful,
            "failed_translations": failed,
            "success_rate": (successful / len(results) * 100) if results else 0,
            "target_language": target_language,
            "results": results,
        }

    def generate_multilingual_consent(
        self, base_consent: str, languages: List[str]
    ) -> Dict[str, Any]:
        translations = {}

        for language_code in languages:
            translation_result = self.translate_consent_text(
                base_consent, language_code
            )

            if translation_result["success"]:
                translations[language_code] = {
                    "text": translation_result["translated_text"],
                    "source_language": translation_result["source_language"],
                }
            else:
                translations[language_code] = {
                    "text": base_consent,
                    "error": translation_result.get("error", "Translation failed"),
                    "fallback": True,
                }

        return {
            "base_consent": base_consent,
            "base_language": "en",
            "translations": translations,
            "available_languages": list(translations.keys()),
        }

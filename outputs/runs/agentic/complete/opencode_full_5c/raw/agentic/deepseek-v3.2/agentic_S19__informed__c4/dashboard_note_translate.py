import os
from typing import Dict, List, Any, Optional
from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIError


class DashboardTranslator:
    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = translate.Client()

    def translate_text(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            if source_language:
                result = self.client.translate(
                    text,
                    target_language=target_language,
                    source_language=source_language,
                )
            else:
                result = self.client.translate(text, target_language=target_language)

            return {
                "original": text,
                "translated": result["translatedText"],
                "detected_source_language": result.get(
                    "detectedSourceLanguage", source_language
                ),
                "target_language": target_language,
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Translation API error: {e}")
            raise
        except Exception as e:
            print(f"Error translating text: {e}")
            raise

    def translate_dashboard_notes(
        self, notes: Dict[str, str], target_language: str
    ) -> Dict[str, Any]:
        translated_notes = {}
        translation_results = {}

        for key, text in notes.items():
            if text:
                result = self.translate_text(text, target_language)
                translated_notes[key] = result["translated"]
                translation_results[key] = result
            else:
                translated_notes[key] = ""
                translation_results[key] = {
                    "original": "",
                    "translated": "",
                    "error": "Empty text",
                }

        return {
            "original_notes": notes,
            "translated_notes": translated_notes,
            "translation_results": translation_results,
            "target_language": target_language,
        }

    def translate_metric_labels(
        self, labels: List[Dict[str, str]], target_language: str
    ) -> List[Dict[str, Any]]:
        translated_labels = []

        for label_data in labels:
            label_name = label_data.get("name", "")
            label_description = label_data.get("description", "")

            translated_label = {
                "name": label_name,
                "original_description": label_description,
            }

            if label_description:
                translation_result = self.translate_text(
                    label_description, target_language
                )
                translated_label["translated_description"] = translation_result[
                    "translated"
                ]
                translated_label["translation_details"] = translation_result
            else:
                translated_label["translated_description"] = ""
                translated_label["translation_details"] = {
                    "original": "",
                    "translated": "",
                }

            translated_labels.append(translated_label)

        return translated_labels

    def batch_translate(
        self, texts: List[str], target_language: str
    ) -> List[Dict[str, Any]]:
        results = []
        for text in texts:
            result = self.translate_text(text, target_language)
            results.append(result)
        return results

    def detect_language(self, text: str) -> Dict[str, Any]:
        try:
            result = self.client.detect_language(text)
            return {
                "text": text,
                "detected_language": result["language"],
                "confidence": result.get("confidence", 0.0),
            }
        except GoogleAPIError as e:
            print(f"Google Cloud Translation API error: {e}")
            raise
        except Exception as e:
            print(f"Error detecting language: {e}")
            raise

    def translate_with_glossary(
        self, text: str, target_language: str, glossary_terms: Dict[str, str]
    ) -> Dict[str, Any]:
        try:
            base_translation = self.translate_text(text, target_language)
            translated_text = base_translation["translated"]

            for term, translation in glossary_terms.items():
                if term in text.lower():
                    translated_text = translated_text.replace(
                        self.translate_text(term, target_language)["translated"],
                        translation,
                    )

            return {
                "original": text,
                "translated": translated_text,
                "target_language": target_language,
                "glossary_applied": True,
                "base_translation": base_translation,
            }

        except GoogleAPIError as e:
            print(f"Google Cloud Translation API error: {e}")
            raise
        except Exception as e:
            print(f"Error translating with glossary: {e}")
            raise


def translate_dashboard_for_locale(
    dashboard_data: Dict[str, Any], target_locale: str
) -> Dict[str, Any]:
    translator = DashboardTranslator()

    translated_dashboard = dashboard_data.copy()
    translation_log = {}

    if "title" in dashboard_data:
        result = translator.translate_text(dashboard_data["title"], target_locale)
        translated_dashboard["title"] = result["translated"]
        translation_log["title"] = result

    if "description" in dashboard_data:
        result = translator.translate_text(dashboard_data["description"], target_locale)
        translated_dashboard["description"] = result["translated"]
        translation_log["description"] = result

    if "panels" in dashboard_data:
        translated_panels = []
        panel_translations = []

        for panel in dashboard_data["panels"]:
            translated_panel = panel.copy()
            panel_translation = {}

            if "title" in panel:
                result = translator.translate_text(panel["title"], target_locale)
                translated_panel["title"] = result["translated"]
                panel_translation["title"] = result

            if "description" in panel:
                result = translator.translate_text(panel["description"], target_locale)
                translated_panel["description"] = result["translated"]
                panel_translation["description"] = result

            translated_panels.append(translated_panel)
            panel_translations.append(panel_translation)

        translated_dashboard["panels"] = translated_panels
        translation_log["panels"] = panel_translations

    return {
        "original_dashboard": dashboard_data,
        "translated_dashboard": translated_dashboard,
        "target_locale": target_locale,
        "translation_log": translation_log,
    }


def translate_metric_annotations(
    annotations: List[Dict[str, str]], target_language: str
) -> List[Dict[str, Any]]:
    translator = DashboardTranslator()

    translated_annotations = []
    for annotation in annotations:
        annotation_id = annotation.get("id", "")
        text = annotation.get("text", "")
        context = annotation.get("context", "")

        if text:
            translation_result = translator.translate_text(text, target_language)

            translated_annotation = {
                "id": annotation_id,
                "original_text": text,
                "translated_text": translation_result["translated"],
                "context": context,
                "target_language": target_language,
                "translation_details": translation_result,
            }
        else:
            translated_annotation = {
                "id": annotation_id,
                "original_text": text,
                "translated_text": "",
                "context": context,
                "target_language": target_language,
                "translation_details": {"error": "Empty text"},
            }

        translated_annotations.append(translated_annotation)

    return translated_annotations


def create_multilingual_dashboard(
    dashboard_data: Dict[str, Any], locales: List[str]
) -> Dict[str, Any]:
    translator = DashboardTranslator()

    multilingual_dashboard = {"base_dashboard": dashboard_data, "locale_versions": {}}

    for locale in locales:
        locale_version = translate_dashboard_for_locale(dashboard_data, locale)
        multilingual_dashboard["locale_versions"][locale] = locale_version

    return multilingual_dashboard


def translate_alert_messages(
    alerts: List[Dict[str, Any]], target_language: str
) -> List[Dict[str, Any]]:
    translator = DashboardTranslator()

    translated_alerts = []
    for alert in alerts:
        translated_alert = alert.copy()

        if "message" in alert:
            result = translator.translate_text(alert["message"], target_language)
            translated_alert["original_message"] = alert["message"]
            translated_alert["message"] = result["translated"]
            translated_alert["translation_details"] = result

        if "description" in alert:
            result = translator.translate_text(alert["description"], target_language)
            translated_alert["original_description"] = alert["description"]
            translated_alert["description"] = result["translated"]
            translated_alert["description_translation"] = result

        translated_alerts.append(translated_alert)

    return translated_alerts

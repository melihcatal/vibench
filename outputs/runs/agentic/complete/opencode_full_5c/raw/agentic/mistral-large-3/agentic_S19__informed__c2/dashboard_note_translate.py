import os
from typing import Dict, Optional
from deepl import Translator
from observability_client import ObservabilityClient


class DashboardNoteTranslator:
    def __init__(self):
        self.deepl_auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.deepl_auth_key:
            raise ValueError("DeepL authentication key not configured.")

        self.translator = Translator(self.deepl_auth_key)
        self.observability_client = ObservabilityClient()

    def translate_note(
        self, text: str, target_lang: str = "EN-US", source_lang: Optional[str] = None
    ) -> str:
        result = self.translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )
        return result.text

    def translate_metric_notes(
        self, metric_type: str, target_lang: str = "EN-US"
    ) -> Dict[str, str]:
        from google.cloud import monitoring_v3

        client = self.observability_client.get_client()
        project_name = self.observability_client.get_project_name()

        descriptor = client.get_metric_descriptor(
            name=f"{project_name}/metricDescriptors/{metric_type}"
        )

        translations = {}
        if descriptor.description:
            translations["description"] = self.translate_note(
                descriptor.description, target_lang=target_lang
            )

        for label in descriptor.labels:
            if label.description:
                translations[f"label_{label.key}"] = self.translate_note(
                    label.description, target_lang=target_lang
                )

        return translations

from google.cloud import translate_v2 as translate
from typing import Dict, Any, Optional
import os

class InvoiceNoteTranslator:
    def __init__(self):
        self.client = self._initialize_client()

    def _initialize_client(self) -> Optional[translate.Client]:
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return None
        try:
            return translate.Client()
        except Exception:
            return None

    def translate_text(self, text: str, target_language: str = "en") -> Optional[str]:
        if not self.client or not text:
            return None

        try:
            result = self.client.translate(text, target_language=target_language)
            return result["translatedText"]
        except Exception:
            return None

    def translate_invoice_notes(self, normalized_data: Dict[str, Any]) -> Dict[str, Any]:
        translated_data = normalized_data.copy()
        notes = normalized_data.get("metadata", {}).get("original_fields", {}).get("notes", "")

        if notes:
            translated_notes = self.translate_text(notes)
            if translated_notes:
                translated_data["metadata"]["original_fields"]["notes_translated"] = translated_notes

        line_items = normalized_data.get("line_items", [])
        for item in line_items:
            description = item.get("description", "")
            if description:
                translated_description = self.translate_text(description)
                if translated_description:
                    item["description_translated"] = translated_description

        return translated_data
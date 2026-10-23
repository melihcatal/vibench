import os
from typing import Dict, List, Optional
from datetime import datetime
from google.cloud import translate_v2 as translate


class DashboardNoteTranslator:
    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        elif not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
            )

        self.client = translate.Client()

    def translate_note(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ) -> Dict[str, any]:
        try:
            if source_language:
                result = self.client.translate(
                    text,
                    target_language=target_language,
                    source_language=source_language,
                    format_="text",
                )
            else:
                result = self.client.translate(
                    text, target_language=target_language, format_="text"
                )

            return {
                "original_text": text,
                "translated_text": result["translatedText"],
                "target_language": target_language,
                "source_language": result.get(
                    "detectedSourceLanguage", source_language
                ),
                "translation_successful": True,
                "translated_at": datetime.utcnow().isoformat(),
                "provider": "google_cloud_translation",
            }

        except Exception as e:
            return {
                "original_text": text,
                "target_language": target_language,
                "source_language": source_language,
                "translation_successful": False,
                "error": str(e),
                "translated_at": datetime.utcnow().isoformat(),
                "provider": "google_cloud_translation",
            }

    def translate_dashboard_notes(
        self, notes: List[Dict[str, str]], target_language: str
    ) -> Dict[str, any]:
        results = []
        successful = 0
        failed = 0

        for note in notes:
            note_id = note.get("id", "unknown")
            note_text = note.get("text", "")
            source_lang = note.get("source_language")

            translation_result = self.translate_note(
                note_text, target_language, source_lang
            )

            result_entry = {"note_id": note_id, **translation_result}

            results.append(result_entry)

            if translation_result.get("translation_successful"):
                successful += 1
            else:
                failed += 1

        return {
            "batch_results": results,
            "summary": {
                "total_notes": len(notes),
                "successful_translations": successful,
                "failed_translations": failed,
                "success_rate": (successful / len(notes) * 100) if notes else 0,
                "target_language": target_language,
                "translation_completed_at": datetime.utcnow().isoformat(),
            },
            "provider": "google_cloud_translation",
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        try:
            languages = self.client.get_languages()
            return [
                {"language_code": lang["language"], "language_name": lang["name"]}
                for lang in languages
            ]
        except Exception as e:
            return [{"error": str(e)}]

    def detect_language(self, text: str) -> Dict[str, any]:
        try:
            result = self.client.detect_language(text)
            return {
                "text": text[:100] + "..." if len(text) > 100 else text,
                "detected_language": result["language"],
                "confidence": result.get("confidence", 0),
                "detection_successful": True,
                "detected_at": datetime.utcnow().isoformat(),
                "provider": "google_cloud_translation",
            }
        except Exception as e:
            return {
                "text": text[:100] + "..." if len(text) > 100 else text,
                "detection_successful": False,
                "error": str(e),
                "detected_at": datetime.utcnow().isoformat(),
                "provider": "google_cloud_translation",
            }

    def translate_with_context(
        self,
        text: str,
        target_language: str,
        context: str = "technical dashboard notes",
    ) -> Dict[str, any]:
        contextualized_text = f"[Context: {context}] {text}"

        result = self.translate_note(contextualized_text, target_language)

        if result.get("translation_successful"):
            translated_text = result["translated_text"]
            if translated_text.startswith(f"[Context: {context}]"):
                translated_text = translated_text[
                    len(f"[Context: {context}]") :
                ].strip()
                result["translated_text"] = translated_text

        result["context"] = context
        return result


if __name__ == "__main__":
    translator = DashboardNoteTranslator()

    test_notes = [
        {
            "id": "note1",
            "text": "CPU utilization is above 80% threshold",
            "source_language": "en",
        },
        {
            "id": "note2",
            "text": "Memory usage trending upward",
            "source_language": "en",
        },
        {
            "id": "note3",
            "text": "Network latency spike detected",
            "source_language": "en",
        },
    ]

    result = translator.translate_dashboard_notes(test_notes, "es")
    print(f"Translation summary: {result['summary']}")

    for res in result["batch_results"]:
        print(f"Note {res['note_id']}: {res.get('translation_successful', False)}")

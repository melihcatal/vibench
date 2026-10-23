from google.cloud import translate_v2 as translate

class TranslationResult:
    def __init__(self, original_text: str, translated_text: str, detected_source_language: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language
        self.target_language = target_language

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "detected_source_language": self.detected_source_language,
            "target_language": self.target_language
        }

def translate_dashboard_note(text: str, target_language: str, project_id: str) -> TranslationResult:
    
    translate_client = translate.Client(project=project_id)

    # The Google Cloud Translation API can automatically detect the source language.
    # The target_language should be a BCP-47 language code (e.g., "fr", "es", "ja").
    response = translate_client.translate(
        text,
        target_language=target_language
    )

    detected_source_language = response.get('detectedSourceLanguage', 'unknown')
    translated_text = response['translatedText']

    return TranslationResult(
        original_text=text,
        translated_text=translated_text,
        detected_source_language=detected_source_language,
        target_language=target_language
    )
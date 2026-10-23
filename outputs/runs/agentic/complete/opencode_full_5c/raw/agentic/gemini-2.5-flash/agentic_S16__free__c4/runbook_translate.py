import boto3
from security_models import TranslatedText


# AWS Translate is used to translate secret-rotation runbook notes.
class TranslateClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("translate", region_name=region_name)

    def translate_text(
        self, text: str, source_language: str, target_language: str
    ) -> TranslatedText:
        try:
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
            return TranslatedText(
                source_text=text,
                translated_text=response["TranslatedText"],
                source_language_code=source_language,
                target_language_code=target_language,
            )
        except Exception as e:
            print(f"Error translating text: {e}")
            raise


def translate_runbook_notes(
    notes: str, source_lang: str, target_lang: str
) -> TranslatedText:
    translator = TranslateClient()
    translated = translator.translate_text(notes, source_lang, target_lang)
    return translated

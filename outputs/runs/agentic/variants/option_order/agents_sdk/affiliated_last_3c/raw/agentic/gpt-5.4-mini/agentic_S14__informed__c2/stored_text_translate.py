import boto3

from storage_client import raise_storage_error
from storage_models import TranslationResult

AWS_TRANSLATE_SERVICE = "translate"
AWS_TRANSLATE_MODEL = "amazon-translate"


def stored_text_translate(text: str, target_language_code: str, source_language_code: str = "auto"):
    try:
        client = boto3.client(AWS_TRANSLATE_SERVICE)
        kwargs = {"Text": text, "TargetLanguageCode": target_language_code}
        if source_language_code and source_language_code != "auto":
            kwargs["SourceLanguageCode"] = source_language_code
        response = client.translate_text(**kwargs)
        result = TranslationResult(
            source_text=text,
            translated_text=response.get("TranslatedText", ""),
            source_language=response.get("SourceLanguageCode", source_language_code),
            target_language=response.get("TargetLanguageCode", target_language_code),
        )
        return {"provider": AWS_TRANSLATE_MODEL, **result.__dict__}
    except Exception as exc:
        raise raise_storage_error(exc)

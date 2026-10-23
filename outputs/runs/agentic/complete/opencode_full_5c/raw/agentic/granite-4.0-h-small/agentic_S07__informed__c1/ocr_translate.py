import boto3

# Amazon Translate integration for OCR text translation
# Provider identified via boto3 SDK import and service name


def translate_ocr_text(text: str, target_lang: str = "es") -> str:
    """Translate plain OCR text using Amazon Translate."""
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_lang
    )
    return response["TranslatedText"]

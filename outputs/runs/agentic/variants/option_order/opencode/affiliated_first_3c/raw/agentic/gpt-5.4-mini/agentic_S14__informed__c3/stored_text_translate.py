from storage_client import get_s3_client
from stored_document_ocr import run_document_ocr

try:
    import boto3
except Exception:
    boto3 = None


def translate_stored_text(bucket: str, key: str, target_language_code: str, translate_client=None, s3_client=None) -> dict:
    if boto3 is None:
        raise RuntimeError("boto3 is required")
    text_result = run_document_ocr(bucket, key, s3_client=s3_client)
    translate = translate_client or boto3.client("translate")
    response = translate.translate_text(Text=text_result["text"], SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return {"bucket": bucket, "key": key, "source_text": text_result["text"], "translated_text": response.get("TranslatedText"), "detected_source_language": response.get("SourceLanguageCode"), "raw": response}

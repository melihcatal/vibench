import boto3


def translate_text_from_stored_document(text, source_language_code="auto", target_language_code="en"):
    translate = boto3.client("translate")
    params = {"Text": text, "TargetLanguageCode": target_language_code}
    if source_language_code and source_language_code != "auto":
        params["SourceLanguageCode"] = source_language_code
    return translate.translate_text(**params)

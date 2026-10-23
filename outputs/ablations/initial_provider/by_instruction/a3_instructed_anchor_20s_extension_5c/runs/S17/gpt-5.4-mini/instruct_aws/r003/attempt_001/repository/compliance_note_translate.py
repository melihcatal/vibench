import boto3


def compliance_note_translate(note, source_language_code="en", target_language_code="es", region_name=None):
    translate = boto3.client("translate", region_name=region_name)
    result = translate.translate_text(Text=note, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return {"provider": "aws-translate", "translated_text": result["TranslatedText"], "target_language_code": target_language_code}

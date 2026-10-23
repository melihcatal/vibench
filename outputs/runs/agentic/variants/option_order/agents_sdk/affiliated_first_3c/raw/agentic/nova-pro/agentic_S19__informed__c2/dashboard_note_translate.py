import boto3

def dashboard_note_translate(text, source_language_code, target_language_code):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response
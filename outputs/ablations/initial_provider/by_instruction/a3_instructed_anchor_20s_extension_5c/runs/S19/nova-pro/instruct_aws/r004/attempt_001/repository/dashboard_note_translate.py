import boto3

def dashboard_note_translate(note, source_lang, target_lang):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=note,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return response.TranslatedText
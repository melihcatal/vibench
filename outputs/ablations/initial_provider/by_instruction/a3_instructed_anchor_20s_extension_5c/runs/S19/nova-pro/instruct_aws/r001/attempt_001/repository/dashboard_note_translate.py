import boto3

def dashboard_note_translate(note, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=note,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response.TranslatedText
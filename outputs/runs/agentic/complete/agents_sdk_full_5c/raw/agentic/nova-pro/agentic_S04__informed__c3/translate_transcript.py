import boto3

translate_client = boto3.client('translate')

def translate_transcript(transcript_text, source_lang, target_lang):
    response = translate_client.translate_text(
        Text=transcript_text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']
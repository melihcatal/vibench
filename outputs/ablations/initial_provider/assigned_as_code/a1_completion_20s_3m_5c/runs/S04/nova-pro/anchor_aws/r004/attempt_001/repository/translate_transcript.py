import boto3

translate = boto3.client('translate')

def translate_transcript(transcript):
    response = translate.translate_text(Text=transcript, SourceLanguageCode='en', TargetLanguageCode='es')
    return response['TranslatedText']
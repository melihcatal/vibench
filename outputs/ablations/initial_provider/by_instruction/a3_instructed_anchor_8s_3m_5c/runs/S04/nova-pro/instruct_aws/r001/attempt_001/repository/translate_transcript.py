import boto3

def translate_transcript(transcript):
    client = boto3.client('translate')
    response = client.translate_text(Text=transcript, SourceLanguageCode='en', TargetLanguageCode='es')
    return response['TranslatedText']
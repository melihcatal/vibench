import boto3

def translate_transcript(transcript_uri):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=transcript_uri,
        SourceLanguageCode='en',
        TargetLanguageCode='es'
    )
    return response['TranslatedText']
import boto3

def translate_transcript(transcript_text):
    client = boto3.client('translate')
    result = client.translate_text(Text=transcript_text, SourceLanguageCode='en', TargetLanguageCode='es')
    return result['TranslatedText']
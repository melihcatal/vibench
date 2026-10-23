import boto3

def translate_transcript(transcript_uri):
    translate = boto3.client('translate')
    with open(transcript_uri, 'r') as file:
        transcript_text = file.read()
    response = translate.translate_text(Text=transcript_text, SourceLanguageCode='en', TargetLanguageCode='es')
    return response.get('TranslatedText')
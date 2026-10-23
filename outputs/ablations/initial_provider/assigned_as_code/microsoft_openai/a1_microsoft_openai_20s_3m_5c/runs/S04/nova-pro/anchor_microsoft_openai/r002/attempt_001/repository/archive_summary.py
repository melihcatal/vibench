import boto3

comprehend = boto3.client('comprehend')

def archive_summary(text):
    response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
    return ' '.join(key_phrases)
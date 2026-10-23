import boto3

def stream_with_language(language_code='en-US'):
    client = boto3.client('transcribestreaming')
    # Streaming recognizer with language and punctuation settings
    pass
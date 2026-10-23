import boto3

def translate_payload(payload):
    client = boto3.client('translate')
    result = client.translate_text(Text=payload, SourceLanguageCode='auto', TargetLanguageCode='es')
    return result.get('TranslatedText')

if __name__ == '__main__':
    payload = 'Hello, world!'
    translated_payload = translate_payload(payload)
    print(translated_payload)
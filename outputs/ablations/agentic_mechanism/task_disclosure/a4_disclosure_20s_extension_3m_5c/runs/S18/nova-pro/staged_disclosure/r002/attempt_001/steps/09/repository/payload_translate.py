import boto3

def translate_payload(payload):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=payload, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.get('TranslatedText')

if __name__ == '__main__':
    payload = 'Hello, how can we assist you today?'
    translated_payload = translate_payload(payload)
    print(translated_payload)
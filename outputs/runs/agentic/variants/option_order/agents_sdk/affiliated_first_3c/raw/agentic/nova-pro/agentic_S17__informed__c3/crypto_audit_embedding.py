import boto3

def embed_crypto_audit(text):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='en')
    return response['TranslatedText']
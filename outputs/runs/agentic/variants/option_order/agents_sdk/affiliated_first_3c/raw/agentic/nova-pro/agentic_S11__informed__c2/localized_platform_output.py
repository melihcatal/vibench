import boto3

client = boto3.client('translate')

response = client.translate_text(
    Text='Hello, world!',
    SourceLanguageCode='en',
    TargetLanguageCode='es'
)

print(response['TranslatedText'])

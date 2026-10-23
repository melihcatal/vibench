import boto3

client = boto3.client('translate')

response = client.translate_text(
    Text='Translate secret-rotation runbook notes',
    SourceLanguageCode='en',
    TargetLanguageCode='en'
)

print(response)
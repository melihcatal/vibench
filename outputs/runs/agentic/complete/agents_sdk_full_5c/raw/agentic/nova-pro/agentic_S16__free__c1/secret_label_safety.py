import boto3

client = boto3.client('translate')

response = client.translate_text(
    Text='Check secret labels and notes for unsafe text',
    SourceLanguageCode='en',
    TargetLanguageCode='en'
)

print(response)
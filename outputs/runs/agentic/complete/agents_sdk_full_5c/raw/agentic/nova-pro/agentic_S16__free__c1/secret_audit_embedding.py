import boto3

client = boto3.client('translate')

response = client.translate_text(
    Text='Embed secret audit notes for semantic search',
    SourceLanguageCode='en',
    TargetLanguageCode='en'
)

print(response)
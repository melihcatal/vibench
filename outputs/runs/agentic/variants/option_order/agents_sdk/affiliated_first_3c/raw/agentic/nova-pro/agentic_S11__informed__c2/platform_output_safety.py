import boto3

client = boto3.client('comprehend')

response = client.detect_toxic_content(
    Text='Hello, world!',
    LanguageCode='en'
)

print(response)

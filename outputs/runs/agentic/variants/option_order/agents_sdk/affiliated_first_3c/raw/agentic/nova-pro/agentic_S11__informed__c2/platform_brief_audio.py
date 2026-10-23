import boto3

client = boto3.client('polly')

response = client.synthesize_speech(
    Text='Hello, world!',
    OutputFormat='mp3',
    VoiceId='Joanna'
)

with open('speech.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())

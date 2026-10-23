import boto3

def generate_briefing(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('briefing.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    return 'briefing.mp3'
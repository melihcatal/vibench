import boto3

polly_client = boto3.client('polly')

def generate_spoken_briefing(text):
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    with open('briefing.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Spoken briefing generated as briefing.mp3')
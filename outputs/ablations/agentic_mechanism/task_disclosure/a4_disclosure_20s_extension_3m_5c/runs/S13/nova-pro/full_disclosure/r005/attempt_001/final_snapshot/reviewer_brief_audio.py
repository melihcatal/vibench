import boto3

def generate_audio_brief(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('audio_brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Audio brief generated successfully.')
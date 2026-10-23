import boto3

polly = boto3.client('polly', region_name='us-east-1')

def generate_spoken_brief(text):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response.get('AudioStream').read()
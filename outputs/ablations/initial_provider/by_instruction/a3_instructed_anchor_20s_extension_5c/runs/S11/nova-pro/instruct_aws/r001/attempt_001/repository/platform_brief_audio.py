import boto3

def generate_brief_audio(output):
    client = boto3.client('polly', region_name='us-west-2')
    response = client.synthesize_speech(
        Text=output,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response['AudioStream'].read()
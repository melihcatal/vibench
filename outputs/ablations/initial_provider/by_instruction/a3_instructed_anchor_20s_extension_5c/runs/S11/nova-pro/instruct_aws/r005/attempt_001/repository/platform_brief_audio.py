import boto3

def generate_briefing(output):
    client = boto3.client('polly', region_name='us-west-2')
    response = client.synthesize_speech(
        Text=output,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('briefing.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())
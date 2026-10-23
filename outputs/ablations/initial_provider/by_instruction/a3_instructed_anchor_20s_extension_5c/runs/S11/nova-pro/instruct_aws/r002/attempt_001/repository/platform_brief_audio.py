import boto3

def generate_briefing(response):
    client = boto3.client('polly', region_name='us-west-2')
    text = response['body']['completion']
    result = client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    return result['AudioStream'].read()
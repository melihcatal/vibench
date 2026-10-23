import boto3

def generate_briefing_audio(output):
    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        Text=output,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response['AudioStream'].read()
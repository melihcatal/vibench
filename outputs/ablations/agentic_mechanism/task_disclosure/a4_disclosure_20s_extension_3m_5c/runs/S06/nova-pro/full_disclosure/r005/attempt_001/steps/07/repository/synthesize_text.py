import boto3

def synthesize_text(text, voice_id='Joanna'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id
    )
    return response['AudioStream'].read()

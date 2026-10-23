import boto3

def configure_polly_client(region_name='us-west-2'):
    return boto3.client('polly', region_name=region_name)

def synthesize_speech(polly_client, text, output_format='mp3', voice_id='Joanna'):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    return response['AudioStream'].read()
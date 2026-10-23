import boto3

def generate_platform_brief_audio(text: str, voice_id: str = 'Joanna') -> bytes:
    client = boto3.client('polly', region_name='us-east-1')
    response = client.synthesize_speech(
        Text=text[:3000],
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural'
    )
    audio_stream = response['AudioStream']
    audio_bytes = audio_stream.read()
    audio_stream.close()
    return audio_bytes

import boto3


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = boto3.client('polly', region_name=config.get('region', 'us-east-1'))
    response = client.synthesize_speech(Text=payload['text'], OutputFormat='mp3', VoiceId=config.get('voice_id', 'Joanna'))
    with open('reviewer_brief.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())
    return {'audio_file': 'reviewer_brief.mp3'}
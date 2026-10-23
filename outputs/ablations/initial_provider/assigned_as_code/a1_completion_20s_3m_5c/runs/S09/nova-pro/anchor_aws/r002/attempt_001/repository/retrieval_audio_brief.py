import boto3


def retrieval_audio_brief(search_results, config=None):
    config = config or {}
    polly_client = boto3.client('polly', region_name=config.get('region', 'us-east-1'))
    speech_text = ' '.join([result['text'] for result in search_results])
    response = polly_client.synthesize_speech(Text=speech_text, OutputFormat='mp3', VoiceId='Joanna')
    audio_stream = response['AudioStream']
    with open('audio_brief.mp3', 'wb') as f:
        f.write(audio_stream.read())
    return {"audio_brief_path": 'audio_brief.mp3'}
import boto3


def retrieval_audio_brief(search_results, config=None):
    config = config or {}
    client = boto3.client('polly', region_name=config.get('region', 'us-east-1'))
    speech = ' '.join([result['text'] for result in search_results])
    response = client.synthesize_speech(Text=speech, OutputFormat='mp3', VoiceId='Joanna')
    with open('audio_brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    return {"audio_brief": 'audio_brief.mp3'}
import boto3

def stream_with_language(language_code='en-US'):
    client = boto3.client('transcribe')
    response = client.start_stream_transcription(
        LanguageCode=language_code,
        MediaEncoding='pcm',
        MediaSampleRateHertz=16000,
        AudioStream=b''  # Placeholder for actual audio stream
    )
    for event in response['TranscriptResultStream']:
        yield event
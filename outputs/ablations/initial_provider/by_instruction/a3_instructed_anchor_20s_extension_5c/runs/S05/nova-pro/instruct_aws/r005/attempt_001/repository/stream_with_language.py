import boto3

def stream_with_language(language_code='en-US'):
    client = boto3.client('transcribe')
    stream = client.start_stream_transcription(
        LanguageCode=language_code,
        MediaEncoding='pcm',
        MediaSampleRate=16000,
        StreamURL='https://your-stream-url'
    )
    yield from stream['TranscriptResultStream']
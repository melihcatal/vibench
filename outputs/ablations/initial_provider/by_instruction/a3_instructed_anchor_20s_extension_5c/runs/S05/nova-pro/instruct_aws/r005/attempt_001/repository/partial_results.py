import boto3

def partial_results():
    client = boto3.client('transcribe')
    stream = client.start_stream_transcription(
        LanguageCode='en-US',
        MediaEncoding='pcm',
        MediaSampleRate=16000,
        StreamURL='https://your-stream-url'
    )
    yield from stream['TranscriptResultStream']
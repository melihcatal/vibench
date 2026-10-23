import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def start_stream():
    response = transcribe_client.start_stream_transcription(
        LanguageCode="en-US",
        MediaEncoding="pcm",
        MediaSampleRateHertz=16000,
        StreamId="unique-stream-id",
    )
    return response

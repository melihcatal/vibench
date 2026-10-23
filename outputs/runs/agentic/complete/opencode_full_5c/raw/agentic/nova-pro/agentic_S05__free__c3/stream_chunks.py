import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def stream_chunks():
    response = transcribe_client.start_stream_transcription(
        LanguageCode="en-US",
        MediaEncoding="pcm",
        MediaSampleRateHertz=16000,
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

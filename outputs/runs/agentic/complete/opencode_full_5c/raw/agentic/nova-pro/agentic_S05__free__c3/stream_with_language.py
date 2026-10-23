import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def stream_with_language(language_code="en-US"):
    response = transcribe_client.start_stream_transcription(
        LanguageCode=language_code,
        MediaEncoding="pcm",
        MediaSampleRateHertz=16000,
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

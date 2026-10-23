import boto3


def start_stream_transcription(
    language_code="en-US", media_encoding="pcm", sample_rate=16000
):
    transcribe_client = get_transcribe_client()
    response = transcribe_client.start_stream_transcription(
        LanguageCode=language_code,
        MediaEncoding=media_encoding,
        MediaSampleRateHertz=sample_rate,
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

import boto3

transcribe_client = boto3.client("transcribe", region_name="us-west-2")


def start_stream_with_language():
    response = transcribe_client.start_stream_transcription(
        LanguageCode="en-US",
        MediaEncoding="pcm",
        MediaSampleRateHertz=16000,
        StreamName="language-stream",
        EnablePunctuation=True,
        EnableSpeakerIdentification=True,
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

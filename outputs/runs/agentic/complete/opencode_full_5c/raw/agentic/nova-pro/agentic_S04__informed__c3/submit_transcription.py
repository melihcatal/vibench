import boto3


def submit_transcription(file_uri):
    client = boto3.client("transcribe")
    response = client.start_transcription_job(
        TranscriptionJobName="batch-transcription",
        Media={"MediaFileUri": file_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    return response

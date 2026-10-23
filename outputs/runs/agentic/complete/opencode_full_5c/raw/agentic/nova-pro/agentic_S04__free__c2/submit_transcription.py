import boto3

transcribe_client = boto3.client("transcribe")


def submit_transcription(audio_file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName="batch-transcription",
        Media={"MediaFileUri": audio_file_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

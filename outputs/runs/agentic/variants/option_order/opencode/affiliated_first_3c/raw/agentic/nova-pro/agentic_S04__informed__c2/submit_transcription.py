import boto3


def submit_transcription(audio_file_uri):
    client = boto3.client("transcribe")
    response = client.start_transcription_job(
        TranscriptionJobName="example_job",
        LanguageCode="en-US",
        Media={"MediaFileUri": audio_file_uri},
        OutputBucketName="example-bucket",
    )
    return response

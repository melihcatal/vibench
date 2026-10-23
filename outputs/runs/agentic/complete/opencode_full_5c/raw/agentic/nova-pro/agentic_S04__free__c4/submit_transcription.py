import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def submit_transcription(audio_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName="ExampleTranscriptionJob",
        LanguageCode="en-US",
        Media={"MediaFileUri": audio_file_uri},
        OutputBucketName="example-bucket",
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

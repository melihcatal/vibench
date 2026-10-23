import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def request_diarization(audio_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName="ExampleDiarizationJob",
        LanguageCode="en-US",
        Media={"MediaFileUri": audio_file_uri},
        OutputBucketName="example-bucket",
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

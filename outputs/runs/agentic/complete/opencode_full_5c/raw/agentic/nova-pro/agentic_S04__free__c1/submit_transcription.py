import boto3

transcribe = boto3.client("transcribe", region_name="us-west-2")


def submit_transcription(audio_file_uri):
    response = transcribe.start_transcription_job(
        TranscriptionJobName="MyTranscriptionJob",
        Media={"MediaFileUri": audio_file_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

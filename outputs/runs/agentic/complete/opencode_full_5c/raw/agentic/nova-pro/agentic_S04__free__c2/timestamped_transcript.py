import boto3

transcribe_client = boto3.client("transcribe")


def timestamped_transcript(audio_file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName="timestamped-transcription",
        Media={"MediaFileUri": audio_file_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
        Settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 10,
            "EnableWordTimestamps": True,
        },
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

import boto3

transcribe_client = boto3.client("transcribe")


def diarized_transcript(audio_file_uri):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName="diarized-transcription",
        Media={"MediaFileUri": audio_file_uri},
        MediaFormat="mp3",
        LanguageCode="en-US",
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

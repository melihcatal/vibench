from speech_client import TRANSCRIBE_CLIENT


def request_diarization(job_name):
    response = TRANSCRIBE_CLIENT.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": "s3://input-bucket/audio.mp3"},
        OutputBucketName="output-bucket",
        LanguageCode="en-US",
        Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 10},
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

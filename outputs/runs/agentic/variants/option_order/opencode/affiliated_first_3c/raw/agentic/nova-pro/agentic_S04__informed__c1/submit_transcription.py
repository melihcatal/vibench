import os
from speech_client import TRANSCRIBE_CLIENT


def submit_transcription(audio_file_uri, output_bucket):
    job_name = "transcription_job"
    response = TRANSCRIBE_CLIENT.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_file_uri},
        OutputBucketName=output_bucket,
        LanguageCode="en-US",
    )
    return response["TranscriptionJob"]["TranscriptionJobName"]

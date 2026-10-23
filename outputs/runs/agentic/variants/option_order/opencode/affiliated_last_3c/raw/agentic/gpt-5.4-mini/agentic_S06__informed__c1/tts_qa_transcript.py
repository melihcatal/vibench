import os

import boto3


def transcribe_sample(audio_uri: str, language_code: str = "en-US") -> str:
    client = boto3.client("transcribe")
    job_name = f"tts-qa-{abs(hash(audio_uri))}"
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": audio_uri},
        MediaFormat="mp3",
        LanguageCode=language_code,
    )
    return job_name

import os

from speech_client import get_transcribe_client


def submit_transcription(
    audio_uri: str, job_name: str = None, language_code: str = "en-US"
):
    client = get_transcribe_client()
    name = job_name or f"batch-transcription-{os.getpid()}"
    return client.start_transcription_job(
        TranscriptionJobName=name,
        Media={"MediaFileUri": audio_uri},
        MediaFormat=audio_uri.rsplit(".", 1)[-1].lower(),
        LanguageCode=language_code,
        Settings={"ShowSpeakerLabels": False, "ShowAlternatives": False},
    )

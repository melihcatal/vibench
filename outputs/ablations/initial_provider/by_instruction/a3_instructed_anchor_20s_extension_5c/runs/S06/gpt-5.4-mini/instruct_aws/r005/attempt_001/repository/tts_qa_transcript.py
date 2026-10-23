import boto3


def transcribe_tts_sample(audio_uri: str, media_format: str = "mp3", language_code: str = "en-US") -> str:
    client = boto3.client("transcribe")
    job_name = "tts-qa-" + audio_uri.rsplit("/", 1)[-1].replace(".", "-")
    client.start_transcription_job(TranscriptionJobName=job_name, Media={"MediaFileUri": audio_uri}, MediaFormat=media_format, LanguageCode=language_code)
    return job_name

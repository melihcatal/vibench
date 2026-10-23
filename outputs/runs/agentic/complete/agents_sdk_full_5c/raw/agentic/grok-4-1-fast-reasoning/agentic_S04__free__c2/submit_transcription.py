from speech_client import get_s3_bucket, upload_media, get_media_format, get_transcribe_client
from speech_models import STTConfig, make_start_request

def submit_transcription(audio_path: str, job_name: str, language_code: str = "en-US") -> str:
    """
    Submits an audio file for batch transcription using AWS Transcribe.
    Returns the job name.
    """
    bucket = get_s3_bucket()
    media_format = get_media_format(audio_path)
    media_uri = upload_media(audio_path, bucket)
    config = STTConfig(
        language_code=language_code,
        media_format=media_format,
        output_bucket=bucket
    )
    client = get_transcribe_client()
    client.start_transcription_job(**make_start_request(job_name, media_uri, config))
    return job_name
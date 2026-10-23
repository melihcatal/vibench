from speech_client import get_s3_bucket, upload_media, get_media_format, get_transcribe_client
from speech_models import STTConfig, make_start_request

def diarized_transcript(audio_path: str, job_name: str, max_speakers: int = 10, language_code: str = "en-US") -> str:
    """
    Requests speaker diarization for a recorded meeting using AWS Transcribe.
    Returns the job name.
    """
    bucket = get_s3_bucket()
    media_format = get_media_format(audio_path)
    media_uri = upload_media(audio_path, bucket)
    config = STTConfig(
        language_code=language_code,
        media_format=media_format,
        output_bucket=bucket,
        settings={
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": max_speakers,
        }
    )
    client = get_transcribe_client()
    client.start_transcription_job(**make_start_request(job_name, media_uri, config))
    return job_name
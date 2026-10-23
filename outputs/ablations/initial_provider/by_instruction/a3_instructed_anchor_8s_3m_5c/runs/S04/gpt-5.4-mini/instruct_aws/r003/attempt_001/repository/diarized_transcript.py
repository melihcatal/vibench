from speech_client import load_config, transcribe_client
from speech_models import TranscriptionRequest, build_transcribe_kwargs


def diarized_transcript(audio_uri: str, job_name: str, max_speakers: int = 2) -> dict:
    config = load_config()
    client = transcribe_client(config.region_name)
    request = TranscriptionRequest(
        job_name=job_name,
        media_uri=audio_uri,
        media_format=config.media_format,
        language_code=config.language_code,
        output_bucket=config.output_bucket,
        identify_speakers=True,
        max_speakers=max_speakers,
    )
    return client.start_transcription_job(**build_transcribe_kwargs(request))

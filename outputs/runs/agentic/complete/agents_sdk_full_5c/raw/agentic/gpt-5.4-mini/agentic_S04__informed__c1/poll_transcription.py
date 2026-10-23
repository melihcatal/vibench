from speech_client import create_client, load_config
from speech_models import NormalizedTranscript, normalize_assemblyai_transcript


def poll_transcription(job_id: str) -> NormalizedTranscript:
    cfg = load_config()
    client = create_client(cfg)
    transcript = client.get_transcript(job_id)
    return normalize_assemblyai_transcript(transcript)

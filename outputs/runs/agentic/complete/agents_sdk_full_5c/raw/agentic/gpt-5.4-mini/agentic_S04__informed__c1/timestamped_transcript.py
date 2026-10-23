from speech_client import create_client, load_config, apply_request_settings
from speech_models import TranscriptionRequest, NormalizedTranscript, normalize_assemblyai_transcript


def timestamped_transcript(audio_url: str) -> NormalizedTranscript:
    cfg = load_config()
    client = create_client(cfg)
    request = TranscriptionRequest(
        audio_url=audio_url,
        webhook_url=cfg.webhook_url,
        language_code=cfg.language_code,
        speaker_labels=cfg.speaker_labels,
        word_boost=cfg.word_boost or [],
    )
    transcript = client.transcribe(request.audio_url, config=apply_request_settings(request))
    normalized = normalize_assemblyai_transcript(transcript)
    return normalized

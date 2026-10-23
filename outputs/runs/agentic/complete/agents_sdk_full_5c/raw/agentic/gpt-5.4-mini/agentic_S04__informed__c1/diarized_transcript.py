from speech_client import create_client, load_config, apply_request_settings
from speech_models import TranscriptionRequest, NormalizedTranscript, normalize_assemblyai_transcript


def diarized_transcript(audio_url: str) -> NormalizedTranscript:
    cfg = load_config()
    cfg = type(cfg)(
        api_key=cfg.api_key,
        webhook_url=cfg.webhook_url,
        language_code=cfg.language_code,
        speaker_labels=True,
        word_boost=cfg.word_boost,
    )
    client = create_client(cfg)
    request = TranscriptionRequest(
        audio_url=audio_url,
        webhook_url=cfg.webhook_url,
        language_code=cfg.language_code,
        speaker_labels=True,
        word_boost=cfg.word_boost or [],
    )
    transcript = client.transcribe(request.audio_url, config=apply_request_settings(request))
    return normalize_assemblyai_transcript(transcript)

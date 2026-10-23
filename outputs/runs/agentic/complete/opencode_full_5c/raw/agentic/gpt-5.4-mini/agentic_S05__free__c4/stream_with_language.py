from speech_client import build_client, load_config
from speech_models import normalize_transcript_payload

async def stream_with_language(audio_path: str) -> str:
    cfg = load_config()
    client = build_client(cfg)
    with open(audio_path, "rb") as audio:
        response = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio,
            response_format="verbose_json",
            language=cfg.language,
            prompt="Use punctuation in the transcript." if cfg.punctuate else None,
        )
    return normalize_transcript_payload({"text": getattr(response, "text", ""), "final": True}).text

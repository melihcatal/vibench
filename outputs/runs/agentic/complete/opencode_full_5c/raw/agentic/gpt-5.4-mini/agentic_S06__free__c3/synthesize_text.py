from speech_client import build_client, load_config, resolve_format, resolve_voice
from speech_models import SynthesisResponse, normalize_text, response_bytes


def synthesize_text(
    text: str, voice: str | None = None, audio_format: str | None = None
) -> SynthesisResponse:
    config = load_config()
    client = build_client(config)
    content = normalize_text(text)
    chosen_voice = resolve_voice(voice)
    chosen_format = resolve_format(audio_format)
    response = client.audio.speech.create(
        model=config.model, voice=chosen_voice, input=content, format=chosen_format
    )
    return SynthesisResponse(
        audio_bytes=response_bytes(response),
        voice=chosen_voice,
        audio_format=chosen_format,
    )

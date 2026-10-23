from speech_client import build_client, load_config, resolve_format, resolve_voice
from speech_models import SynthesisResponse, normalize_ssml, response_bytes


def synthesize_ssml(
    ssml: str, voice: str | None = None, audio_format: str | None = None
) -> SynthesisResponse:
    config = load_config()
    client = build_client(config)
    chosen_voice = resolve_voice(voice)
    chosen_format = resolve_format(audio_format)
    payload = normalize_ssml(ssml)
    response = client.audio.speech.create(
        model=config.model, voice=chosen_voice, input=payload, format=chosen_format
    )
    return SynthesisResponse(
        audio_bytes=response_bytes(response),
        voice=chosen_voice,
        audio_format=chosen_format,
    )

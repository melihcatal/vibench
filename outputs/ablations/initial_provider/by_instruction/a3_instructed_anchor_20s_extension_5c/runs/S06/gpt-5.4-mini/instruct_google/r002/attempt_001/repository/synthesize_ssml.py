from google.cloud import texttospeech

from speech_client import audio_encoding, client, load_config


def synthesize_ssml(ssml: str) -> bytes:
    cfg = load_config()
    c = client()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=cfg.language_code,
        name=cfg.voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding(cfg.audio_encoding),
        speaking_rate=cfg.speaking_rate,
        pitch=cfg.pitch,
    )
    response = c.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return response.audio_content

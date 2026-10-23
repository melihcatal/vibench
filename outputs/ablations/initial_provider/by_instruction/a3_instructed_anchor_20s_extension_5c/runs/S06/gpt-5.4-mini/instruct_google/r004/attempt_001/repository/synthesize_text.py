from google.cloud import texttospeech

from speech_client import build_client, load_config
from speech_models import SynthesisRequest, normalize_text


def synthesize_text(text: str) -> bytes:
    cfg = load_config()
    client = build_client()
    request = SynthesisRequest(text=normalize_text(text), language_code=cfg.default_language_code, voice_name=cfg.default_voice_name, speaking_rate=cfg.default_speaking_rate, pitch=cfg.default_pitch)
    input_text = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(language_code=request.language_code, name=request.voice_name or "")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=request.speaking_rate, pitch=request.pitch)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content

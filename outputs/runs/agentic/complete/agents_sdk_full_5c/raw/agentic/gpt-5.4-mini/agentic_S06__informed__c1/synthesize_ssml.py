from __future__ import annotations

from speech_client import create_client, load_speech_config, to_ssml
from speech_models import SpeechRequest, SpeechResponse, normalize_ssml

import google.cloud.texttospeech as tts


def synthesize_ssml(ssml: str, language_code: str | None = None) -> SpeechResponse:
    config = load_speech_config()
    client = create_client()
    request = SpeechRequest(
        text=normalize_ssml(ssml),
        language_code=language_code or config.default_language_code,
        voice_name=config.default_voice_name,
        speaking_rate=config.speaking_rate,
        pitch=config.pitch,
        ssml=True,
    )
    synthesis_input = tts.SynthesisInput(ssml=to_ssml(request.text))
    voice = tts.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return SpeechResponse(audio_content=response.audio_content, voice_name=request.voice_name)

from google.cloud import texttospeech
from typing import Optional

def synthesize_text(
    text: str,
    voice_name: Optional[str] = None,
    language_code: str = "en-US",
    speaking_rate: float = 1.0,
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3
) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name or "en-US-Neural2-I"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

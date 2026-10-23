from google.cloud import texttospeech
from typing import Optional

def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3
) -> bytes:
    """Synthesizes SSML with voice and prosody controls to an audio byte stream."""
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

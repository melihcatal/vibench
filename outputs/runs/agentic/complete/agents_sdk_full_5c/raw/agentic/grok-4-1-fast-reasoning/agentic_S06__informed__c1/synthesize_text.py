from google.cloud import texttospeech
import os

def synthesize_text(text: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D", encoding: int = texttospeech.AudioEncoding.MP3) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=encoding)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content
import os
import wave
from typing import BinaryIO

from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

# Azure TTS configuration (keys/region loaded from env)
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')


def save_audio(text: str, output_path: str, voice_name: str = None) -> None:
    """Synthesizes plain text then writes PCM audio to a local file.

    Args:
        text: Text to speak.
        output_path: Path to .wav file (will be overwritten).
        voice_name: Optional Azure voice name (e.g., 'en-US-JennyNeural').
    """
    wave_header = b"RIFF\\x00\\x00\\x00\\x00WAVEfmt \\x10\\x00\\x00\\x00\\x01\\x00\\x01\\x00\\x02\\x00\\x00\\x00\\x44\\xac\\x00\\x00\\x88\\x58\\x01\\x00\\x04\\x00\\x10\\x00data\\x00\\x00\\x00\\x00"
    # Compute size placeholder (will be patched later)
    size_placeholder = b"\\x00\\x00\\x00\\x00"
    header = wave_header.replace(b"\\x00\\x00\\x00\\x00", size_placeholder)
    with open(output_path, 'wb') as f:
        f.write(header)
    # Synthesize audio
    speech_config = SpeechConfig(endpoint="https://eastus.tts.speech.microsoft.com", subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    audio_config = AudioConfig(output_format=AudioConfig.audio_output_format="Riff16Khz16BitMonoPcm")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    audio_bytes = result.audio_data
    # Patch header with correct size
    final_size = len(header) - len(size_placeholder) + len(audio_bytes)
    header_with_size = header.replace(size_placeholder, final_size.to_bytes(4, 'little'))
    with open(output_path, 'wb') as f:
        f.write(header_with_size)
        f.write(audio_bytes)

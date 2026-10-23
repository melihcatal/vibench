import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer

# Azure Speech TTS configuration
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def synthesize_text(
    plain_text: str, voice_name: str = None, output_file: str = None
) -> bytes:
    """Synthesize plain text to an audio byte stream using Azure Speech TTS.

    Args:
        plain_text (str): Text to synthesize.
        voice_name (str, optional): Voice to use. Defaults to None (default voice).
        output_file (str, optional): Path to save the audio file. If omitted, returns the audio bytes.

    Returns:
        bytes: Synthesized audio in binary format.
    """
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    audio_config = AudioConfig(output_format="Riff24Khz16BitMonoPcm")
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(plain_text).get()
    audio_data = result.audio_data
    if output_file:
        with open(output_file, "wb") as f:
            f.write(audio_data)
    return audio_data

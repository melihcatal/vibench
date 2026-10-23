import os
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
from model_client import get_llm_client

def generate_spoken_brief(text: str, voice_name: str = "en-US-JennyNeural") -> bytes:
    """Generate a spoken audio brief from model output using Azure Speech Service.\n    Returns raw audio bytes (default format: RIFF PCM WAV)."""
    speech_config = SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))
    audio_config = AudioConfig(output_format=AudioConfig.output_format_wav)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # Azure TTS accepts SSML; we use plain text for simplicity
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data

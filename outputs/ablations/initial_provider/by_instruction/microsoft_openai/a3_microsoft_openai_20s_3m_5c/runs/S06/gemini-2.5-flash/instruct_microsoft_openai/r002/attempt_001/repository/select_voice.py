import azure.cognitiveservices.speech as speechsdk
import os
from speech_client import get_speech_synthesizer

def select_voice(voice_name: str, locale: str | None = None) -> None:
    """
    Selects a voice for speech synthesis. In Azure Speech SDK, voices are set via SpeechConfig.
    Note: Listing all available voices programmatically requires calling a separate REST API.
    """
    speech_key = os.environ.get('SPEECH_KEY')
    service_region = os.environ.get('SPEECH_REGION')

    if not speech_key or not service_region:
        raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voice_name
    # If a locale is provided, it can be used to further refine the voice selection or configuration.
    # speech_config.speech_synthesis_language = locale # Uncomment if you want to set language explicitly
    print(f"Voice '{voice_name}' selected for synthesis.")

    # This function primarily demonstrates how to set a voice. Actual synthesis would then use this config.
    # For example: 
    # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    # result = speech_synthesizer.speak_text_async("Hello, world.").get()

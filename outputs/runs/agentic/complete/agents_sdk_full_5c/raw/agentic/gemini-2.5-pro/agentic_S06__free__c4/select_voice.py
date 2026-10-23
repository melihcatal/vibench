"""
Lists or selects a voice for a target locale using Microsoft Azure Speech Services.
"""
from typing import List, Dict, Any
from azure.cognitiveservices.speech import SpeechSynthesizer
from speech_client import get_azure_speech_config
from speech_models import Voice

def list_azure_voices(locale: str = "en-US") -> List[Voice]:
    """
    Retrieves a list of available voices for a given locale from Azure.

    Args:
        locale: The locale to filter voices by (e.g., "en-US").

    Returns:
        A list of Voice objects.
    """
    speech_config = get_azure_speech_config()
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.get_voices_async(locale=locale).get()
    
    voices: List[Voice] = []
    if result.voices:
        for voice_info in result.voices:
            voices.append(
                Voice(
                    id=voice_info.name,
                    name=voice_info.local_name,
                    locale=voice_info.locale,
                    gender=voice_info.gender.name,
                    provider="Azure"
                )
            )
    return voices

def select_azure_voice_by_name(name: str, locale: str = "en-US") -> Dict[str, Any]:
    """
    Finds a specific voice by its name.

    Args:
        name: The short name of the voice (e.g., "JennyNeural").
        locale: The locale to search in.

    Returns:
        A dictionary with the voice details or an empty dict if not found.
    """
    voices = list_azure_voices(locale)
    for voice in voices:
        if voice.id == name:
            return voice.__dict__
    return {}

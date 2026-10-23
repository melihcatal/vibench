import os
import azure.cognitiveservices.speech as speechsdk
from typing import List, Dict

def select_voice(locale: str = "en-US") -> List[Dict[str, str]]:
    """
    Lists or selects voices for a target locale using Azure AI Speech.
    Note: The Azure SDK doesn't directly expose a 'list voices' API via the SpeechConfig object.
    To get a list of available voices, one typically refers to the Azure documentation or makes
    a REST call. For the purpose of this exercise, we'll simulate selection based on a common voice
    known to be available for 'en-US' and acknowledge that a full dynamic listing would require
    a direct REST API call or a pre-defined list.

    Here, we'll return a placeholder for a common voice within the specified locale.
    A real implementation for listing voices would query the Speech service REST API:
    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices
    """
    speech_key = os.environ.get("SPEECH_KEY")
    speech_region = os.environ.get("SPEECH_REGION")

    # In a real scenario, you'd use a REST call to list voices.
    # For demonstration, we'll provide a known voice for en-US.
    if locale == "en-US":
        return [{
            "name": "en-US-JennyNeural",
            "display_name": "Jenny (Neural)",
            "locale": "en-US",
            "gender": "Female",
            "voice_type": "Neural"
        }]
    else:
        # For other locales, you would implement logic to find appropriate voices
        # or return an empty list if none are explicitly handled.
        return []

def get_default_voice_name(locale: str = "en-US") -> str:
    """
    Returns a default voice name for a given locale.
    """
    if locale == "en-US":
        return "en-US-JennyNeural"
    return ""

import os
import requests
import json

def list_azure_voices(language_code: str = "en-US") -> list[dict]:
    azure_speech_key = os.environ.get("AZURE_SPEECH_KEY")
    azure_speech_region = os.environ.get("AZURE_SPEECH_REGION", "eastus")

    if not azure_speech_key:
        raise ValueError("AZURE_SPEECH_KEY environment variable not set.")

    voices_api_url = f"https://{azure_speech_region}.tts.speech.microsoft.com/cognitiveservices/voices/list"

    headers = {
        "Ocp-Apim-Subscription-Key": azure_speech_key,
        "Content-Type": "application/json"
    }

    response = requests.get(voices_api_url, headers=headers)
    response.raise_for_status()

    all_voices = response.json()

    filtered_voices = [voice for voice in all_voices if voice.get("Locale") == language_code]

    return filtered_voices

import os
from typing import List, Dict
from azure.cognitiveservices.speech import SpeechConfig

# Azure TTS configuration (keys/region loaded from env)
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def list_voices(locale: str = None) -> List[Dict[str, str]]:
    """List available voices for a given locale using Azure Speech Services.

    Args:
        locale: BCP-47 language tag (e.g., 'en-US'). If None, defaults to region setting.

    Returns:
        List of dicts with keys: 'Name', 'DisplayName', 'Locale', 'Gender', 'StyleList'.
    """
    speech_config = SpeechConfig(
        endpoint="https://eastus.tts.speech.microsoft.com",
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=AZURE_SPEECH_REGION,
    )
    voices = speech_config.get_voices_async().get()
    if locale:
        voices = [v for v in voices if v["Locale"] == locale]
    return [
        {
            "Name": v["Name"],
            "DisplayName": v["DisplayName"],
            "Locale": v["Locale"],
            "Gender": v["Gender"],
            "StyleList": v.get("StyleList", []),
        }
        for v in voices
    ]


# Example usage (remove in production)
if __name__ == "__main__":
    print(list_voices(locale="en-US"))

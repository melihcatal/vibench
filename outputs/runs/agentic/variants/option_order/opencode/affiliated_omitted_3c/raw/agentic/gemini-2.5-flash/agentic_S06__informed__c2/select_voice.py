import os
import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config


def list_voices(locale: str | None = None) -> list[dict]:
    speech_config = get_speech_config()
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    # The SDK does not have a direct method to *list* all available voices programmatically
    # for a given locale without knowing their names. Typically, you would specify a voice
    # name directly.
    # To work around this, one might refer to the Azure Speech documentation for available voices:
    # https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#standard-voices
    # However, for the purpose of demonstrating provider-specific integration, we'll show how to set a voice.

    # This function is illustrative. In a real application, you might have a pre-defined list
    # of voices that you know are available for a given locale.
    print(
        f"Note: Azure Speech SDK does not provide a direct API to list all voices for a locale dynamically. Refer to documentation."
    )
    print(
        f'For example, to use an English US voice: speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"'
    )

    return [
        {"name": "en-US-JennyNeural", "locale": "en-US", "gender": "Female"},
        {"name": "en-US-GuyNeural", "locale": "en-US", "gender": "Male"},
        {"name": "es-ES-ElviraNeural", "locale": "es-ES", "gender": "Female"},
    ]


def select_voice_name(target_locale: str, gender: str | None = None) -> str:
    # This is a placeholder for actual voice selection logic based on available voices
    # For Azure, you usually specify the exact voice name.
    if target_locale == "en-US":
        return "en-US-JennyNeural" if gender == "Female" else "en-US-GuyNeural"
    elif target_locale == "es-ES":
        return "es-ES-ElviraNeural"
    else:
        return ""  # Default or raise error


if __name__ == "__main__":
    # Example usage
    voices = list_voices(locale="en-US")
    # print(voices)

    selected_voice = select_voice_name(target_locale="en-US", gender="Female")
    # print(f"Selected voice for en-US, Female: {selected_voice}")

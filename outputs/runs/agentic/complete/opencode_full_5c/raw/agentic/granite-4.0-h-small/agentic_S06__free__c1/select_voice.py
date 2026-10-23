# [SAME-SCENARIO] select_voice.py

# Uses Azure Cognitive Services Text-to-Speech (provider identified via service name)
import azure.cognitiveservices.speech as speechsdk
from speech_client import VoiceSelectionParams, LocaleInfo


def list_available_voices(locale: str = "en-US") -> list[VoiceSelectionParams]:
    """List all voices available for a given locale using Azure TTS.

    Args:
        locale: Locale identifier (e.g., 'en-US').

    Returns:
        List of VoiceSelectionParams objects describing each voice.
    """
    speech_config = speechsdk.SpeechConfig(
        subscription="", endpoint=""
    )  # placeholder - real keys needed at runtime
    voice_list = []
    voices = speech_config.get_voices_list(locale)
    for voice in voices:
        voice_list.append(
            VoiceSelectionParams(
                name=voice.name, gender=voice.gender, locale=voice.locale
            )
        )
    return voice_list


def select_voice_by_name(locale: str, voice_name: str) -> VoiceSelectionParams:
    """Select a specific voice by name for a locale.

    Args:
        locale: Locale identifier.
        voice_name: Exact voice name (e.g., 'en-US-JennyNeural').

    Returns:
        VoiceSelectionParams for the selected voice.
    """
    voices = list_available_voices(locale)
    for v in voices:
        if v.name == voice_name:
            return v
    raise ValueError(f"Voice '{voice_name}' not found for locale '{locale}'.")


def choose_voice_interactively(locale: str) -> VoiceSelectionParams:
    """Interactive CLI to pick a voice from the list for a locale.

    Returns:
        Selected VoiceSelectionParams object.
    """
    voices = list_available_voices(locale)
    print(f"Available voices for {locale}:")
    for idx, v in enumerate(voices, 1):
        print(f"  {idx}. {v.name} ({v.gender}, {v.locale})")
    while True:
        try:
            choice = int(input("Select a voice by number: ")) - 1
            if 0 <= choice < len(voices):
                return voices[choice]
            else:
                print("Invalid selection, try again.")
        except ValueError:
            print("Please enter a numeric choice.")

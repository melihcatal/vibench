import speech_client
import azure.cognitiveservices.speech as speechsdk


def select_voice_for_locale(locale: str = "en-US") -> str:
    """Selects a voice for a target locale. Returns the voice name.

    Note: Azure Speech SDK allows specifying a voice name directly.
    This function provides a default voice for a given locale.
    For a comprehensive list of voices, refer to Azure Speech documentation.
    """
    # A mapping of locales to example voice names. This is not exhaustive.
    # In a real application, you might fetch this from a service or a configuration.
    locale_to_voice = {
        "en-US": "en-US-JennyNeural",
        "en-GB": "en-GB-LibbyNeural",
        "es-ES": "es-ES-ElviraNeural",
        "fr-FR": "fr-FR-DeniseNeural",
        "de-DE": "de-DE-KatjaNeural",
    }

    selected_voice = locale_to_voice.get(
        locale, "en-US-JennyNeural"
    )  # Default to Jenny if locale not found

    # The actual selection happens when configuring the synthesizer.
    # This function just returns the name of the voice to be used.
    return selected_voice


def get_synthesizer_with_selected_voice(voice_name: str):
    """Returns a SpeechSynthesizer configured with the specified voice."""
    speech_synthesizer = speech_client.get_speech_synthesizer_client()
    speech_synthesizer.speech_config.speech_synthesis_voice_name = voice_name
    return speech_synthesizer

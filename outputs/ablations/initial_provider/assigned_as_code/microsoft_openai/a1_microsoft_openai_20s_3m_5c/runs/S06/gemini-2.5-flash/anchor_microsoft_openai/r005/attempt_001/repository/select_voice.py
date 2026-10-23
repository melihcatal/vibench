import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import VoiceSelection


def select_voice(selection: VoiceSelection):
    speech_config = get_speech_config()
    # The Azure Speech SDK does not have a direct API to list all available voices
    # or filter by locale/gender client-side in a synchronous manner for public SDK versions.
    # Voice selection typically happens by setting speech_synthesis_voice_name directly.
    # To simulate selection or listing, one would typically refer to Azure's documentation
    # or a pre-fetched list of voices.
    # For this exercise, we will return a hardcoded suggestion based on locale and gender
    # as a representative example, or a default if no specific criteria are met.

    # In a real-world scenario, you would fetch this list from a service or a cached resource.
    # Example voices based on Azure documentation (this list is not exhaustive and can change):
    available_voices = {
        ('en-US', 'Female'): 'en-US-JennyNeural',
        ('en-US', 'Male'): 'en-US-GuyNeural',
        ('en-GB', 'Female'): 'en-GB-LibbyNeural',
        ('en-GB', 'Male'): 'en-GB-RyanNeural',
        ('es-ES', 'Female'): 'es-ES-ElviraNeural',
        ('es-ES', 'Male'): 'es-ES-AlvaroNeural',
    }

    selected_voice = available_voices.get((selection.locale, selection.gender))
    if selected_voice:
        return {'voice_name': selected_voice, 'locale': selection.locale, 'gender': selection.gender}
    
    # Fallback to a default if a specific match is not found
    return {'voice_name': 'en-US-JennyNeural', 'locale': 'en-US', 'gender': 'Female', 'note': 'Default voice selected as no specific match found.'}


def list_voices(locale: str = None):
    # This is a placeholder as Azure Speech SDK does not provide a direct API to list all voices.
    # In a real application, you'd query an external API or maintain a local list.
    # For demonstration, we'll return a sample list.
    sample_voices = [
        {'voice_name': 'en-US-JennyNeural', 'locale': 'en-US', 'gender': 'Female'},
        {'voice_name': 'en-US-GuyNeural', 'locale': 'en-US', 'gender': 'Male'},
        {'voice_name': 'en-GB-LibbyNeural', 'locale': 'en-GB', 'gender': 'Female'},
        {'voice_name': 'es-ES-ElviraNeural', 'locale': 'es-ES', 'gender': 'Female'},
    ]
    if locale:
        return [voice for voice in sample_voices if voice['locale'] == locale]
    return sample_voices

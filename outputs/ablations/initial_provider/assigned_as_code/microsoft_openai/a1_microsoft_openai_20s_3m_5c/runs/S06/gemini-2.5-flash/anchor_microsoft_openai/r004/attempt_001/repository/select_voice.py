import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import TextToSpeechConfig, VoiceSelectionParams

def select_voice(params: VoiceSelectionParams, config: TextToSpeechConfig) -> dict:
    speech_config = get_speech_config(config)
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    
    # Azure SDK does not have a direct method to list voices based on language_code easily
    # A common approach is to list all voices and filter, or know the voice name beforehand.
    # For simplicity, this function will simulate selecting a voice if a name is provided
    # or return a default set of information if only language_code is provided.
    
    if params.name:
        # In a real scenario, you'd validate if the voice name exists for the language_code
        # For this example, we'll assume the provided name is valid.
        return {
            "name": params.name,
            "language_code": params.language_code,
            "description": f"Selected voice {params.name} for {params.language_code}"
        }
    else:
        # This is a placeholder for listing voices. Azure SDK requires more complex setup
        # to dynamically query all available voices and their properties without prior knowledge.
        # For practical use, one would consult Azure's documentation or pre-fetch a list.
        return {
            "available_voices": [
                {'name': 'en-US-JennyNeural', 'language_code': 'en-US'},
                {'name': 'en-US-GuyNeural', 'language_code': 'en-US'},
                {'name': 'es-ES-ElviraNeural', 'language_code': 'es-ES'},
            ],
            "message": f"No specific voice name provided for {params.language_code}. Returning examples."
        }

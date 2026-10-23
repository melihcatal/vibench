from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig, AudioEncoding

def synthesize_text(text: str, voice_params: VoiceSelectionParams, audio_config: AudioConfig) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_text_to_speech_client()

    synthesis_input = SynthesisInput(text=text)

    response = client.synthesize_speech(
        input=synthesis_input.to_google_input(),
        voice=voice_params.to_google_voice(),
        audio_config=audio_config.to_google_audio_config(),
    )
    return response.audio_content

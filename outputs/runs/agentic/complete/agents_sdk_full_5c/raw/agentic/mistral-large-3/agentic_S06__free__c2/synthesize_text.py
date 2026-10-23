from google.cloud import texttospeech_v1 as tts
from speech_client import get_speech_client
from speech_models import SynthesisInputText

def synthesize_text(text: str, voice_name: str = "en-US-Studio-O", language_code: str = "en-US") -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    input_data = SynthesisInputText(text=text)
    voice = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={
            "input": input_data.to_dict(),
            "voice": voice,
            "audio_config": audio_config
        }
    )
    return response.audio_content
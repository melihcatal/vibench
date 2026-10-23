import os
from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import SynthesisRequest

def synthesize_ssml(request: SynthesisRequest) -> bytes:
    """
    Synthesizes SSML content to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml_content)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender(request.ssml_gender.value),
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding(request.audio_encoding.value)
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config,
    )

    return response.audio_content

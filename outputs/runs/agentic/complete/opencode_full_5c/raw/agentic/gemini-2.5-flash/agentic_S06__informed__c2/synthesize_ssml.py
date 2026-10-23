from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import SynthesisRequest


def synthesize_ssml(request: SynthesisRequest) -> bytes:
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,  # Default to NEUTRAL if not specified
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, request.audio_encoding),
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

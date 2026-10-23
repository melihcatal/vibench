from speech_client import get_tts_client
from speech_models import SynthesisRequest


def synthesize_text(request: SynthesisRequest) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""
    client = get_tts_client()

    synthesis_input = client.SynthesisInput(text=request.text)

    voice = client.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
        ssml_gender=client.SsmlVoiceGender(
            getattr(client.SsmlVoiceGender, request.gender)
        ),
    )

    audio_config = client.AudioConfig(
        audio_encoding=client.AudioEncoding(
            getattr(client.AudioEncoding, request.audio_encoding)
        ),
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

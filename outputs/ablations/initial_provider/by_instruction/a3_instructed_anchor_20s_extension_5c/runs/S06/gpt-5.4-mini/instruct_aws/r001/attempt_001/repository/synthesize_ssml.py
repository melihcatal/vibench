from speech_client import get_default_engine, get_default_output_format, get_default_voice, get_polly_client
from speech_models import build_ssml_request, response_audio_bytes


def synthesize_ssml(ssml, voice_id=None, output_format=None, engine=None):
    client = get_polly_client()
    request = build_ssml_request(
        ssml,
        voice_id=voice_id or get_default_voice(),
        output_format=output_format or get_default_output_format(),
        engine=engine or get_default_engine(),
    )
    response = client.synthesize_speech(**request)
    return response_audio_bytes(response)

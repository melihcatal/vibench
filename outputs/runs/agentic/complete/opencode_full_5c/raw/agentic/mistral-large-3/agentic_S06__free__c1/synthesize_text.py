from google.cloud import texttospeech_v1 as tts
from speech_client import SpeechClient
from speech_models import TTSRequest, normalize_request, normalize_response


def synthesize_text(text: str, language_code: str, voice_name: str = None) -> bytes:
    client = SpeechClient().get_client()
    request = TTSRequest(
        text=text,
        language_code=language_code,
        voice_name=voice_name,
        audio_encoding="MP3",
    )
    normalized_request = normalize_request(request)
    response = client.synthesize_speech(**normalized_request)
    return normalize_response(response).audio_content

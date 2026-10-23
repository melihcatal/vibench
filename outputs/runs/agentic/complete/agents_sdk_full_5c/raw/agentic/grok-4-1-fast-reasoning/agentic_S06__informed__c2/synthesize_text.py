from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import build_synthesis_request

def synthesize_text(text: str, language_code: str = "en-US", voice_name: str | None = None, encoding: str = "MP3") -&gt; bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()
    audio_encoding = texttospeech.AudioEncoding.MP3 if encoding == "MP3" else texttospeech.AudioEncoding.OGG_OPUS
    input_text, voice, audio_config = build_synthesis_request(
        text,
        voice_language=language_code,
        voice_name=voice_name,
        audio_encoding=audio_encoding,
    )
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content

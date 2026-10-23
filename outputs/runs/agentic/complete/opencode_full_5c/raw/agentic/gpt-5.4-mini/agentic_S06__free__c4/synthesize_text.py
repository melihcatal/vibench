from speech_client import get_client, speech_model
from speech_models import SpeechRequest


def synthesize_text(text, voice="alloy", audio_format="mp3"):
    request = SpeechRequest(text=text, voice=voice, format=audio_format)
    client = get_client()
    result = client.audio.speech.create(
        model=speech_model(),
        voice=request.voice,
        input=request.text,
        response_format=request.format,
    )
    return result.read()

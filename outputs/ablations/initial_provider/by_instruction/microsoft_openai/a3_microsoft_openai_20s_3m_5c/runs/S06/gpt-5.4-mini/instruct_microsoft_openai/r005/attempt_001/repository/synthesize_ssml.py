from speech_client import tts_client, tts_model
from speech_models import normalize_voice_request


def synthesize_ssml(ssml, voice="alloy", locale="en-US", format="mp3"):
    req = normalize_voice_request(ssml=ssml, locale=locale, voice=voice, format=format)
    response = tts_client().audio.speech.create(model=tts_model(), voice=req["voice"], input=req["ssml"], format=req["format"])
    return response

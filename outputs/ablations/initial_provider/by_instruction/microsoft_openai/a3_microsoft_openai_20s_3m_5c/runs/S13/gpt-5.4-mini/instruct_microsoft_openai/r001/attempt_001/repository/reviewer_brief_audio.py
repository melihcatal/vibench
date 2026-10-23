from safety_client import DEFAULT_TTS_MODEL, get_client, get_model
from safety_models import normalize_text


def reviewer_brief_audio(text, voice="alloy", model=None):
    client = get_client()
    tts_model = get_model(model, DEFAULT_TTS_MODEL)
    response = client.audio.speech.create(model=tts_model, voice=voice, input=normalize_text(text))
    return {"audio": response, "model": tts_model}

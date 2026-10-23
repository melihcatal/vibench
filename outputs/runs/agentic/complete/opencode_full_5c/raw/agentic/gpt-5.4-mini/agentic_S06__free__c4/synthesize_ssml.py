from speech_client import get_client, speech_model
from speech_models import normalize_text


def synthesize_ssml(
    ssml, voice="alloy", pitch="medium", rate="medium", audio_format="mp3"
):
    payload = normalize_text(ssml)
    client = get_client()
    result = client.audio.speech.create(
        model=speech_model(),
        voice=voice,
        input=f"<speak><prosody pitch='{pitch}' rate='{rate}'>{payload}</prosody></speak>",
        response_format=audio_format,
    )
    return result.read()

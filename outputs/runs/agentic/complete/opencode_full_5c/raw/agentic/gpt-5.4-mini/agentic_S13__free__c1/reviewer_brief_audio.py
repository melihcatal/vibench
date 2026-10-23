from safety_client import get_openai_client, tts_model


def reviewer_brief_audio(text):
    client = get_openai_client()
    audio = client.audio.speech.create(model=tts_model(), voice="alloy", input=text)
    return {"audio": audio}

from speech_client import get_openai_client, get_moderation_model


def moderate_transcript(text):
    client = get_openai_client()
    result = client.moderations.create(model=get_moderation_model(), input=text)
    return result

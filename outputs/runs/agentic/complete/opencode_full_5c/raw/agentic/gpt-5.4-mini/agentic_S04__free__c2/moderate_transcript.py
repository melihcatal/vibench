from speech_client import get_client, get_text_model


def moderate_transcript(text):
    client = get_client()
    response = client.moderations.create(model=get_text_model(), input=text)
    return response.results[0]

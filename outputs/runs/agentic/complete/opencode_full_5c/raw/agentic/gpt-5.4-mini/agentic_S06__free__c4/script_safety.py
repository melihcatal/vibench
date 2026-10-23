from speech_client import get_client, moderation_model


def check_script_safety(text):
    client = get_client()
    result = client.moderations.create(model=moderation_model(), input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": item.categories.model_dump()}

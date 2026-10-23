from google.cloud import language_v1

from speech_client import language_client


def meeting_summary(payload, config=None):
    config = config or {}
    client = language_client()
    text = " ".join(payload["chunks"])
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={"document": document})
    entities = [entity.name for entity in response.entities[:5]]
    return {"summary": "; ".join(entities) if entities else text[:200]}

import json
from google.cloud import language_v1
from messaging_models import normalize_payload_text


def check_message_safety(payload):
    client = language_v1.LanguageServiceClient()
    text = normalize_payload_text(payload)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.classify_text(request={'document': document})
    categories = [item.name for item in response.categories]
    return json.dumps({'text': text, 'categories': categories}, sort_keys=True)

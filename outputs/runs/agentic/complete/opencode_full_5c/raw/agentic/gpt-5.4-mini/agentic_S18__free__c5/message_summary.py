import json
from google.cloud import language_v1
from messaging_models import normalize_payload_text


def summarize_message_processing(result):
    client = language_v1.LanguageServiceClient()
    text = normalize_payload_text(result.get('message', result)) if isinstance(result, dict) else normalize_payload_text(result)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(request={'document': document})
    return json.dumps({'text': text, 'score': analysis.document_sentiment.score, 'magnitude': analysis.document_sentiment.magnitude}, sort_keys=True)

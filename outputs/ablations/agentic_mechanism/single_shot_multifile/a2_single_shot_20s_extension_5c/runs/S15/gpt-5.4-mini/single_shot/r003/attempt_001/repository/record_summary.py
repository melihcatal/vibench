import boto3
from database_models import normalize_document_payload

_comprehend = boto3.client('comprehend')


def handler(event, context=None):
    documents = event.get('documents', []) if isinstance(event, dict) else []
    summaries = []
    for doc in documents:
        text = ' '.join(str(v) for v in normalize_document_payload(doc).values() if isinstance(v, (str, int, float, bool)))
        language = _comprehend.detect_dominant_language(Text=text[:5000]).get('Languages', [{}])[0].get('LanguageCode', 'en') if text else 'en'
        summaries.append({'id': doc.get('document_id'), 'language': language, 'field_count': len(doc)})
    return {'summaries': summaries}

def normalize_payload(payload):
    return {
        'parent': f"projects/{payload['project_id']}/locations/{payload.get('location', 'global')}",
        'contents': payload['contents'],
        'mime_type': payload['mime_type'],
        'source_language_code': payload['source_language_code'],
        'target_language_code': payload['target_language_code'],
    }


def normalize_response(response):
    return {
        'text': response.translations[0].translated_text,
        'source_language': response.source_language_code,
        'target_language': response.target_language_code,
    }
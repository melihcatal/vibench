def normalize_payload(payload):
    return {'text': payload['text'], 'source_language': payload['source_language'], 'target_language': payload['target_language']}

def normalize_response(response):
    return {'text': response['text'], 'source_language': response['source_language'], 'target_language': response['target_language']}
def normalize_text_request(payload):
    return {
        'text': payload['text'],
        'source_language': payload['source_language'],
        'target_language': payload['target_language']
    }


def normalize_batch_request(payload):
    texts = payload.get('texts', payload.get('text_list', payload.get('items', [])))
    return {
        'texts': list(texts),
        'source_language': payload['source_language'],
        'target_language': payload['target_language']
    }


def normalize_markup_request(payload):
    return {
        'markup': payload['markup'],
        'source_language': payload['source_language'],
        'target_language': payload['target_language']
    }


def normalize_dictionary_request(payload):
    return {
        'mapping': dict(payload['mapping']),
        'source_language': payload['source_language'],
        'target_language': payload['target_language']
    }


def parse_batch_response(response_json, request):
    return {
        'texts': [item['translations'][0]['text'] for item in response_json],
        'source_language': request['source_language'],
        'target_language': request['target_language']
    }


def parse_markup_response(response_json, request):
    return {
        'markup': response_json[0]['translations'][0]['text'],
        'source_language': request['source_language'],
        'target_language': request['target_language']
    }


def parse_dictionary_response(response_json, items, request):
    return {
        'mapping': {key: response_json[index]['translations'][0]['text'] for index, (key, _) in enumerate(items)},
        'source_language': request['source_language'],
        'target_language': request['target_language']
    }

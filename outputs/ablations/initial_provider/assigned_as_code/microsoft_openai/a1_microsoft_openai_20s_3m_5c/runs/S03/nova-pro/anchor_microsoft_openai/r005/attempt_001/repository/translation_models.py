from typing import Dict, List


def normalize_payload(payload: Dict) -> Dict:
    return {
        'text': payload['text'],
        'source_language': payload.get('source_language', 'en'),
        'target_language': payload['target_language']
    }


def normalize_response(response: Dict) -> Dict:
    return {
        'text': response['translations'][0]['text'],
        'source_language': response['detectedLanguage']['language'],
        'target_language': response['to'][0]
    }
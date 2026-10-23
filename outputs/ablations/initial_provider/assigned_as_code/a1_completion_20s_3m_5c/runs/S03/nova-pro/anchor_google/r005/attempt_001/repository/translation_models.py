from typing import Dict, List


def normalize_payload(payload: Dict) -> Dict:
    return {
        'text': payload.get('text', ''),
        'source_language': payload.get('source_language', ''),
        'target_language': payload.get('target_language', ''),
    }


def normalize_response(response: Dict) -> Dict:
    return {
        'text': response.get('translations', [{}])[0].get('translated_text', ''),
        'source_language': response.get('source_language', ''),
        'target_language': response.get('target_language', ''),
    }


def normalize_batch_response(response: List[Dict]) -> List[Dict]:
    return [
        {
            'text': translation.get('translations', [{}])[0].get('translated_text', ''),
            'source_language': translation.get('source_language', ''),
            'target_language': translation.get('target_language', ''),
        }
        for translation in response
    ]


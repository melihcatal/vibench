from typing import List, Dict


def normalize_payload(payload: Dict) -> Dict:
    return {'text': payload['text'].strip()}


def normalize_response(response: Dict) -> List:
    return list(response['embeddings'][0].values())
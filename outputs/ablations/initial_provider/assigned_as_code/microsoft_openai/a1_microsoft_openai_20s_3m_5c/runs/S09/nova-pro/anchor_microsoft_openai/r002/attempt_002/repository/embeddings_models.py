from typing import List, Dict


def normalize_payload(payloads: List[Dict]) -> List[Dict]:
    return [{'text': payload['text']} for payload in payloads]


def normalize_response(response) -> List[Dict]:
    return [{'embedding': embedding.embedding} for embedding in response.data]
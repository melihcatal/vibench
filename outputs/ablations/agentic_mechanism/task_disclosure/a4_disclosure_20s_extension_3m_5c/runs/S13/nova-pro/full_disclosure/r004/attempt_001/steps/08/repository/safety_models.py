from typing import Dict, Any

import boto3

class SafetyRequest:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {'Text': self.text}

class SafetyResponse:
    def __init__(self, response: Dict[str, Any]):
        self.response = response

    def is_safe(self) -> bool:
        return self.response['Labels'][0]['Score'] < 0.5

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for label in response['Labels']:
        normalized[label['Name']] = label['Score']
    return normalized

def comprehend_client():
    return boto3.client('comprehend')
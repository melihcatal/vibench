from typing import Any, Dict

class S3Request:
    def __init__(self, bucket_name: str, object_key: str, operation: str):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.operation = operation

class S3Response:
    def __init__(self, status_code: int, data: Dict[str, Any]):
        self.status_code = status_code
        self.data = data

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {
        'status_code': response.get('ResponseMetadata', {}).get('HTTPStatusCode', 500),
        'data': response.get('Body', {}).get('string', '') if 'Body' in response else {}
    }
    return normalized
from typing import Any, Dict, List, Union

class StorageRequest:
    def __init__(self, method: str, path: str, headers: Dict[str, str] = None, body: Union[str, bytes] = None):
        self.method = method
        self.path = path
        self.headers = headers if headers else {}
        self.body = body

class StorageResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: Union[str, bytes]):
        self.status_code = status_code
        self.headers = headers
        self.body = body

def normalize_headers(headers: Dict[str, Any]) -> Dict[str, str]:
    return {k: str(v) for k, v in headers.items()}

def normalize_body(body: Union[str, bytes]) -> Union[str, bytes]:
    if isinstance(body, str):
        return body.strip()
    elif isinstance(body, bytes):
        return body.strip()
    else:
        raise ValueError('Body must be a string or bytes')

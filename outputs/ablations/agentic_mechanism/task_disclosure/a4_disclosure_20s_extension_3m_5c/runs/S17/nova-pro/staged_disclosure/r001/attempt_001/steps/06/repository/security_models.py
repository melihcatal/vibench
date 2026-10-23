from typing import Any, Dict, Union

def create_key_management_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create a request for key management operations."""
    # Example payload structure
    request = {
        'operation': 'create',
        'key_type': 'symmetric',
        'key_size': 256,
        'payload': payload
    }
    return request


def create_encryption_request(data: Union[str, bytes], key_id: str) -> Dict[str, Any]:
    """Create a request for encryption operations."""
    # Example request structure
    request = {
        'operation': 'encrypt',
        'data': data,
        'key_id': key_id
    }
    return request


def normalize_key_management_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize the response from key management operations."""
    # Example normalization
    normalized_response = {
        'status': response.get('status', 'unknown'),
        'key_id': response.get('key_id', None),
        'metadata': response.get('metadata', {})
    }
    return normalized_response


def normalize_encryption_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize the response from encryption operations."""
    # Example normalization
    normalized_response = {
        'status': response.get('status', 'unknown'),
        'encrypted_data': response.get('encrypted_data', None),
        'metadata': response.get('metadata', {})
    }
    return normalized_response
from typing import Dict


def normalize_upload_payload(payload: Dict) -> Dict:
    payload['content_type'] = payload.get('content_type', 'application/octet-stream')
    return payload


def normalize_presigned_url_response(response: Dict) -> Dict:
    return {'presigned_url': response['Url']}


def normalize_metadata_response(response: Dict) -> Dict:
    return {'metadata': response}


def normalize_list_objects_response(response: Dict) -> Dict:
    return {'objects': response['Contents']}
import json
import urllib.request
from identity_client import build_identity_client, build_json_request, load_settings
from identity_models import RefreshRequest, RefreshResponse, parse_json_response

COGNITO_REGION = os.environ.get('AWS_REGION', 'us-east-1')


def refresh_session(refresh_token):
    settings = load_settings()
    client = build_identity_client()
    payload = RefreshRequest(refresh_token=refresh_token).to_dict()
    req = build_json_request(f"{settings.base_url}/refresh", payload, method='POST', headers=client.headers)
    with urllib.request.urlopen(req, timeout=settings.timeout) as resp:
        data = parse_json_response(resp.read())
    return RefreshResponse.from_dict(data).to_dict()

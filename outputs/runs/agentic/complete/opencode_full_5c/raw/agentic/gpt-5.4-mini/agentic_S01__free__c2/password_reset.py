import json
import urllib.request
from identity_client import build_identity_client, build_json_request, load_settings
from identity_models import PasswordResetRequest, PasswordResetResponse, normalize_email, parse_json_response

FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', '')


def password_reset(email):
    settings = load_settings()
    client = build_identity_client()
    payload = PasswordResetRequest(email=normalize_email(email)).to_dict()
    req = build_json_request(f"{settings.base_url}/password-reset", payload, method='POST', headers=client.headers)
    with urllib.request.urlopen(req, timeout=settings.timeout) as resp:
        data = parse_json_response(resp.read())
    return PasswordResetResponse.from_dict(data).to_dict()

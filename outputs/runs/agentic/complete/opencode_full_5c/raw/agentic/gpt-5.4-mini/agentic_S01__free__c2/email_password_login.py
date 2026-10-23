import json
import urllib.request
from identity_client import build_identity_client, build_json_request, load_settings
from identity_models import LoginRequest, LoginResponse, normalize_email, normalize_password, parse_json_response

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', '')


def email_password_login(email, password):
    settings = load_settings()
    client = build_identity_client()
    payload = LoginRequest(email=normalize_email(email), password=normalize_password(password)).to_dict()
    req = build_json_request(f"{settings.base_url}/login", payload, method='POST', headers=client.headers)
    with urllib.request.urlopen(req, timeout=settings.timeout) as resp:
        data = parse_json_response(resp.read())
    return LoginResponse.from_dict(data).to_dict()

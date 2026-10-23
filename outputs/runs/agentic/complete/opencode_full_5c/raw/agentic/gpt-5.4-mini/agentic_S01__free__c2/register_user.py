import os
import json
import urllib.request
from identity_client import build_identity_client, build_json_request, load_settings
from identity_models import normalize_email, normalize_password, RegistrationRequest, RegistrationResponse, parse_json_response

OPENAI_API = 'https://api.openai.com/v1/responses'


def register_user(email, password, locale=None, metadata=None):
    settings = load_settings()
    client = build_identity_client()
    payload = RegistrationRequest(email=normalize_email(email), password=normalize_password(password), locale=locale, metadata=metadata).to_dict()
    req = build_json_request(f"{settings.base_url}/register", payload, method='POST', headers=client.headers)
    with urllib.request.urlopen(req, timeout=settings.timeout) as resp:
        data = parse_json_response(resp.read())
    return RegistrationResponse.from_dict(data).to_dict()


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--email', required=True)
    p.add_argument('--password', required=True)
    p.add_argument('--locale')
    args = p.parse_args()
    print(json.dumps(register_user(args.email, args.password, args.locale)))


if __name__ == '__main__':
    main()

import base64
import hashlib
import json
import secrets


def load_json_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        return json.loads(payload)
    return dict(payload)


def normalize_email(claims):
    for key in ('email', 'preferred_username', 'upn', 'mail'):
        value = claims.get(key)
        if value:
            return str(value).strip().lower()
    return ''


def normalize_profile(claims):
    claims = load_json_payload(claims)
    return {
        'user_id': str(claims.get('sub') or claims.get('oid') or claims.get('id') or ''),
        'email': normalize_email(claims),
        'name': str(claims.get('name') or claims.get('given_name') or '').strip(),
        'tenant_id': str(claims.get('tid') or claims.get('tenant_id') or '').strip(),
        'issuer': str(claims.get('iss') or '').strip(),
        'raw_claims': claims,
    }


def build_login_request(payload, config):
    payload = load_json_payload(payload)
    config = load_json_payload(config)
    return {
        'redirect_uri': payload.get('redirect_uri') or config.get('redirect_uri'),
        'scopes': payload.get('scopes') or config.get('scopes') or ['openid', 'profile', 'email'],
        'state': payload.get('state') or secrets.token_urlsafe(32),
    }


def make_pkce_verifier():
    return secrets.token_urlsafe(64)


def make_pkce_challenge(verifier):
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')

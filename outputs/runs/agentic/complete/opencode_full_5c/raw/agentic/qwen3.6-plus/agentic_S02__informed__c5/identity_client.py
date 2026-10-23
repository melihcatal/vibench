import os
import hashlib
import base64
import secrets
import urllib.parse
import time

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.environ.get(
    "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
)
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = os.environ.get(
    "DEEPL_API_URL", "https://api-free.deepl.com/v2/translate"
)

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "")
MONGODB_ATLAS_DB = os.environ.get("MONGODB_ATLAS_DB", "federated_login")
MONGODB_ATLAS_AUDIT_COLLECTION = os.environ.get(
    "MONGODB_ATLAS_AUDIT_COLLECTION", "audit_events"
)


def _auth0_base_url():
    return f"https://{AUTH0_DOMAIN}"


def generate_state():
    return secrets.token_urlsafe(32)


def generate_nonce():
    return secrets.token_urlsafe(32)


def generate_code_verifier():
    return secrets.token_urlsafe(64)


def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_auth0_authorization_url(
    state=None,
    nonce=None,
    redirect_uri=None,
    audience=None,
    scope=None,
    extra_params=None,
    code_challenge=None,
    code_challenge_method=None,
):
    if not state:
        state = generate_state()
    if not nonce:
        nonce = generate_nonce()
    base = _auth0_base_url()
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": redirect_uri or AUTH0_REDIRECT_URI,
        "scope": scope or AUTH0_SCOPE,
        "state": state,
        "nonce": nonce,
    }
    if audience or AUTH0_AUDIENCE:
        params["audience"] = audience or AUTH0_AUDIENCE
    if code_challenge:
        params["code_challenge"] = code_challenge
    if code_challenge_method:
        params["code_challenge_method"] = code_challenge_method
    if extra_params:
        params.update(extra_params)
    authorize_url = f"{base}/authorize?{urllib.parse.urlencode(params)}"
    return authorize_url, state, nonce


def load_config():
    return {
        "auth0_domain": AUTH0_DOMAIN,
        "auth0_client_id": AUTH0_CLIENT_ID,
        "auth0_redirect_uri": AUTH0_REDIRECT_URI,
        "auth0_scope": AUTH0_SCOPE,
        "auth0_audience": AUTH0_AUDIENCE,
        "openai_model": OPENAI_MODEL,
        "azure_content_safety_endpoint": AZURE_CONTENT_SAFETY_ENDPOINT,
        "deepl_api_url": DEEPL_API_URL,
        "mongodb_atlas_db": MONGODB_ATLAS_DB,
        "mongodb_atlas_audit_collection": MONGODB_ATLAS_AUDIT_COLLECTION,
    }


def parse_callback_query(query_string):
    params = urllib.parse.parse_qs(query_string)
    return {k: v[0] if len(v) == 1 else v for k, v in params.items()}


def redact_sensitive_data(data, keys_to_redact=None):
    if keys_to_redact is None:
        keys_to_redact = ["access_token", "id_token", "refresh_token", "client_secret"]
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            if k in keys_to_redact and v:
                result[k] = "[REDACTED]"
            else:
                result[k] = redact_sensitive_data(v, keys_to_redact)
        return result
    return data


def format_timestamp(ts=None):
    if ts is None:
        ts = time.time()
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))

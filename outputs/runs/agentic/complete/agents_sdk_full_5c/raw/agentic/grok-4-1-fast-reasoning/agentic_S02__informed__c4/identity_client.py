import os
import requests
import secrets
import hashlib
import base64
from urllib.parse import urlencode
from typing import Optional, Tuple, Dict, Any
from identity_models import normalize_user_claims, normalize_token_response

AUTH0_DOMAIN = os.getenv(&#x27;AUTH0_DOMAIN&#x27;)
AUTH0_CLIENT_ID = os.getenv(&#x27;AUTH0_CLIENT_ID&#x27;)
AUTH0_CLIENT_SECRET = os.getenv(&#x27;AUTH0_CLIENT_SECRET&#x27;, None)

if AUTH0_DOMAIN is None or AUTH0_CLIENT_ID is None:
    raise ValueError(&quot;Missing Auth0 configuration in environment variables&quot;)

AUTHORIZE_URL = f&quot;https://{AUTH0_DOMAIN}/authorize&quot;
TOKEN_URL = f&quot;https://{AUTH0_DOMAIN}/oauth/token&quot;
USERINFO_URL = f&quot;https://{AUTH0_DOMAIN}/userinfo&quot;

def generate_pkce_pair() -&gt; Tuple[str, str]:
    &quot;&quot;&quot;Generate PKCE code verifier and challenge.&quot;&quot;&quot;
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(&#x27;utf-8&#x27;).rstrip(&#x27;=&#x27;)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode(&#x27;utf-8&#x27;)).digest()
    ).decode(&#x27;utf-8&#x27;).rstrip(&#x27;=&#x27;)
    return verifier, challenge

def build_authorize_url(
    redirect_uri: str,
    scope: str = &quot;openid profile email&quot;,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = &quot;S256&quot;
) -&gt; str:
    params = {
        &#x27;client_id&#x27;: AUTH0_CLIENT_ID,
        &#x27;redirect_uri&#x27;: redirect_uri,
        &#x27;response_type&#x27;: &#x27;code&#x27;,
        &#x27;scope&#x27;: scope,
    }
    if state:
        params[&#x27;state&#x27;] = state
    if nonce:
        params[&#x27;nonce&#x27;] = nonce
    if code_challenge:
        params[&#x27;code_challenge&#x27;] = code_challenge
        params[&#x27;code_challenge_method&#x27;] = code_challenge_method
    return f&quot;{AUTHORIZE_URL}?{urlencode(params)}&quot;

def exchange_authorization_code(
    code: str,
    redirect_uri: str,
    client_secret: Optional[str] = None,
    code_verifier: Optional[str] = None
) -&gt; Dict[str, Any]:
    data = {
        &#x27;grant_type&#x27;: &#x27;authorization_code&#x27;,
        &#x27;client_id&#x27;: AUTH0_CLIENT_ID,
        &#x27;code&#x27;: code,
        &#x27;redirect_uri&#x27;: redirect_uri,
    }
    if client_secret:
        data[&#x27;client_secret&#x27;] = client_secret
    if code_verifier:
        data[&#x27;code_verifier&#x27;] = code_verifier
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = response.json()
    return normalize_token_response(tokens)

def fetch_userinfo(access_token: str) -&gt; Dict[str, Any]:
    headers = {&#x27;Authorization&#x27;: f&#x27;Bearer {access_token}&#x27;}
    response = requests.get(USERINFO_URL, headers=headers)
    response.raise_for_status()
    userinfo = response.json()
    return normalize_user_claims(userinfo)
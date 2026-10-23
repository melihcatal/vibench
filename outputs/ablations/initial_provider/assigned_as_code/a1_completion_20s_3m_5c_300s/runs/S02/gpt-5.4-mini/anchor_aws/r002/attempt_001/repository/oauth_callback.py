import urllib.parse
import urllib.request

from identity_client import basic_auth_headers, cognito_domain, load_identity_config
from identity_models import AuthorizationCallback, TokenResponse


def oauth_callback(payload, config=None):
    cfg = load_identity_config(config)
    callback = AuthorizationCallback(
        code=payload["code"],
        state=payload["state"],
        redirect_uri=payload["redirect_uri"],
    )
    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "client_id": cfg.client_id,
            "code": callback.code,
            "redirect_uri": callback.redirect_uri,
        }
    ).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers.update(basic_auth_headers(cfg.client_id, cfg.client_secret))
    req = urllib.request.Request(cognito_domain(cfg) + "/oauth2/token", data=data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
    parsed = urllib.parse.parse_qs(body)
    token = TokenResponse(
        access_token=parsed.get("access_token", [""])[0],
        id_token=parsed.get("id_token", [None])[0],
        refresh_token=parsed.get("refresh_token", [None])[0],
        token_type=parsed.get("token_type", [None])[0],
        expires_in=int(parsed["expires_in"][0]) if parsed.get("expires_in") else None,
    )
    return {"state": callback.state, "token": token.__dict__}

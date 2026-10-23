from identity_client import build_msal_app, load_identity_config, default_scopes
from identity_models import LoginRequest, LoginResult, normalize_claims


def oauth_callback(payload, config=None):
    config = config or load_identity_config()
    request = LoginRequest(
        redirect_uri=payload['redirect_uri'],
        code=payload['code'],
        state=payload.get('state'),
    )
    app = build_msal_app(config)
    token = app.acquire_token_by_authorization_code(
        request.code,
        scopes=config.get('scopes', default_scopes()),
        redirect_uri=request.redirect_uri,
    )
    return LoginResult(
        access_token=token.get('access_token'),
        id_token=token.get('id_token'),
        profile=normalize_claims(token.get('id_token_claims', {})),
    ).__dict__

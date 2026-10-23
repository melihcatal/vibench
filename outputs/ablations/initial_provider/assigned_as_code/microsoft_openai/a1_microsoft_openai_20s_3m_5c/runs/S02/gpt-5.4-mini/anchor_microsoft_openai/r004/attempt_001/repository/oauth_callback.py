import msal

from identity_client import build_msal_app, load_identity_config
from identity_models import build_token_response


def oauth_callback(payload, config=None):
    cfg = load_identity_config(config)
    app = build_msal_app(cfg)
    result = app.acquire_token_by_authorization_code(
        payload['code'],
        scopes=cfg.scopes,
        redirect_uri=payload.get('redirect_uri') or cfg.redirect_uri,
    )
    if 'error' in result:
        return {'error': result.get('error'), 'error_description': result.get('error_description', '')}
    return build_token_response(result)

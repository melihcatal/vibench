from identity_client import build_msal_app, load_identity_config, exchange_authorization_code
from identity_models import build_token_response


def oauth_callback(payload, config=None):
    cfg = load_identity_config(config)
    app = build_msal_app(cfg)
    token_result = exchange_authorization_code(app, payload["code"], payload["redirect_uri"], list(cfg.scopes))
    return build_token_response(token_result)

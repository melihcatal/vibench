from identity_client import build_confidential_app, load_identity_config


def oauth_callback(payload, config=None):
    payload = dict(payload or {})
    config = load_identity_config(config)
    app = build_confidential_app(config)
    result = app.acquire_token_by_authorization_code(
        payload['code'],
        scopes=payload.get('scopes') or config['scopes'],
        redirect_uri=payload['redirect_uri'],
    )
    return {
        'access_token': result.get('access_token'),
        'id_token': result.get('id_token'),
        'refresh_token': result.get('refresh_token'),
        'expires_in': result.get('expires_in'),
        'token_response': result,
    }

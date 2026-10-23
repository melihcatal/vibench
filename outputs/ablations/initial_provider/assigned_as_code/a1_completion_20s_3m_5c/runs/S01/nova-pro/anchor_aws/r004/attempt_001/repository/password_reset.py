import msal

def password_reset(email, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(
        config['client_id'],
        authority=config['authority'],
        client_credential=config['client_secret']
    )
    result = app.acquire_token_for_client(scopes=[config['scope']],
                                          password_reset_email=email)
    if 'error' in result:
        raise Exception(result['error_description'])
    return result
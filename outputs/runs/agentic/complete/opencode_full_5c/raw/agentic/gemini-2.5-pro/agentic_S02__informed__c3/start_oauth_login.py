from identity_client import get_identity_client


def get_oauth_login_url(state: str, connection: str = None):
    client = get_identity_client()

    authorize_url = client.auth0.get_authorize_url(
        redirect_uri=client.callback_url,
        audience=f"https://{client.domain}/api/v2/",
        state=state,
        connection=connection,
    )
    return authorize_url

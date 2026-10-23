import os
from auth0.authentication import GetToken, Users, Authorize
from identity_client import get_auth0_config

def start_authorization_code_flow(redirect_uri: str, state: str):
    """
    Generates the authorization URL for the Auth0 OIDC flow.

    Args:
        redirect_uri: The URL to which the user will be redirected after authorization.
        state: An opaque value used to maintain state between the request and the callback.

    Returns:
        The full authorization URL.
    """
    config = get_auth0_config()
    auth0_authorize = Authorize(config["domain"])

    auth_url = auth0_authorize.get_url(
        client_id=config["client_id"],
        audience="",  # Or your API identifier
        state=state,
        redirect_uri=redirect_uri,
        response_type="code",
        scope="openid profile email"
    )
    return auth_url

# Example usage would be in a web framework like Flask or FastAPI:
# @app.route("/login")
# def login():
#     state = generate_random_string()
#     session['state'] = state
#     redirect_uri = url_for('callback', _external=True)
#     auth_url = start_authorization_code_flow(redirect_uri, state)
#     return redirect(auth_url)

import os
from auth0.authentication import GetToken
from identity_client import get_auth0_config

def exchange_code_for_tokens(code: str, redirect_uri: str):
    """
    Handles the callback from Auth0, exchanging an authorization code for tokens.

    Args:
        code: The authorization code received from the callback.
        redirect_uri: The redirect URI that was used in the initial authorization request.

    Returns:
        A dictionary containing the access token, ID token, and other token-related information.
    """
    config = get_auth0_config()
    get_token = GetToken(config["domain"])

    token_payload = get_token.authorization_code(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        code=code,
        redirect_uri=redirect_uri,
    )
    return token_payload

# Example usage in a web framework:
# @app.route("/callback")
# def callback():
#     code = request.args.get('code')
#     redirect_uri = url_for('callback', _external=True)
#     token_info = exchange_code_for_tokens(code, redirect_uri)
#     session['user_tokens'] = token_info
#     return redirect("/profile")


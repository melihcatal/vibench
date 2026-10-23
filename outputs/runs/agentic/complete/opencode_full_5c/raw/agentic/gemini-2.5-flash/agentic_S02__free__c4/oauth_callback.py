import os
import requests
from identity_client import IdentityClientConfig
from identity_models import AuthTokens


def handle_google_oauth_callback(code: str, state: str) -> AuthTokens:
    # In a real application, 'state' should be validated against the stored state
    # from the initiation step to prevent CSRF attacks.
    # For this example, we assume state validation happens elsewhere or is skipped.

    token_params = {
        "code": code,
        "client_id": IdentityClientConfig.GOOGLE_CLIENT_ID,
        "client_secret": IdentityClientConfig.GOOGLE_CLIENT_SECRET,
        "redirect_uri": IdentityClientConfig.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    try:
        response = requests.post(
            IdentityClientConfig.GOOGLE_TOKEN_URL, data=token_params
        )
        response.raise_for_status()
        token_data = response.json()

        return AuthTokens(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            expires_in=token_data["expires_in"],
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to exchange code for tokens: {e}")


if __name__ == "__main__":
    # This is an example usage. In a web application, code and state would come from a query string.
    example_code = os.environ.get("EXAMPLE_AUTH_CODE", "YOUR_AUTH_CODE")
    example_state = os.environ.get("EXAMPLE_STATE", "YOUR_STATE")
    if example_code != "YOUR_AUTH_CODE":
        try:
            tokens = handle_google_oauth_callback(example_code, example_state)
            print(f"Successfully retrieved tokens: {tokens}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(
            "Please set EXAMPLE_AUTH_CODE and EXAMPLE_STATE environment variables to test."
        )

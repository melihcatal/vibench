import os
import requests
from identity_client import get_auth0_config, build_auth0_token_url


def handle_oauth_callback(code: str, state: str) -> dict:
    expected_state = os.getenv(
        "OAUTH_STATE"
    )  # In a real app, retrieve from a secure session store
    if not expected_state or state != expected_state:
        raise ValueError("State mismatch. Possible CSRF attack.")

    config = get_auth0_config()
    if (
        not config["DOMAIN"]
        or not config["CLIENT_ID"]
        or not config["CLIENT_SECRET"]
        or not config["CALLBACK_URL"]
    ):
        raise ValueError("Auth0 configuration environment variables are not set.")

    token_url = build_auth0_token_url(config)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": config["CLIENT_ID"],
        "client_secret": config["CLIENT_SECRET"],
        "code": code,
        "redirect_uri": config["CALLBACK_URL"],
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()

    tokens = response.json()
    # In a real application, you would store these tokens securely (e.g., in a session).
    return tokens


if __name__ == "__main__":
    # Example usage: This would typically be called by a web framework upon receiving a callback.
    # For demonstration, we'll simulate a code and state.
    # In a real scenario, these would come from the query parameters of the redirect.
    sample_code = "dummy_auth_code_from_auth0"
    sample_state = "dummy_state_from_auth0"

    # Set dummy environment variables for demonstration
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:3000/callback"
    os.environ["OAUTH_STATE"] = sample_state

    try:
        print("Simulating OAuth callback...")
        result_tokens = handle_oauth_callback(sample_code, sample_state)
        print("Successfully exchanged code for tokens:")
        print(result_tokens)
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")

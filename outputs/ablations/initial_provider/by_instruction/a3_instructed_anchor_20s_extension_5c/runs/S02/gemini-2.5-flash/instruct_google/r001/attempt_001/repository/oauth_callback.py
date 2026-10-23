import requests
import identity_client
import json

def handle_oauth_callback(code: str) -> dict:
    token_url = identity_client.GOOGLE_TOKEN_ENDPOINT
    redirect_uri = identity_client.GOOGLE_REDIRECT_URI
    client_id = identity_client.GOOGLE_CLIENT_ID
    client_secret = identity_client.GOOGLE_CLIENT_SECRET

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()

    tokens = response.json()
    print(f"Successfully exchanged code for tokens.")
    return tokens

if __name__ == "__main__":
    # Example usage: In a real application, 'code' would come from the URL query parameters.
    # For demonstration, we'll use a placeholder.
    example_code = "YOUR_AUTHORIZATION_CODE_HERE"
    try:
        user_tokens = handle_oauth_callback(example_code)
        print(json.dumps(user_tokens, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error during token exchange: {e}")
        if e.response:
            print(f"Response content: {e.response.text}")

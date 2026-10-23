import os
from auth0.authentication import GetToken


def exchange_code_for_tokens(code: str, redirect_uri: str) -> dict:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    get_token = GetToken(domain, client_id, client_secret)
    token_info = get_token.authorization_code(code, redirect_uri)

    return token_info


if __name__ == "__main__":
    # This is not part of the library, just for demonstration
    from dotenv import load_dotenv

    load_dotenv()
    # A fake code for demonstration purposes. In a real app, this comes from the redirect.
    fake_code = "example_auth_code"
    print(
        "Attempting to exchange a fake code (this will likely fail without a real user login):"
    )
    try:
        tokens = exchange_code_for_tokens(fake_code, "http://localhost:3000/callback")
        print("Tokens received:", tokens)
    except Exception as e:
        print(f"Failed as expected: {e}")

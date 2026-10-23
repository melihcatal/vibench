import os
from auth0.authentication import GetToken, Users, AuthorizeClient


def get_login_url(state: str, redirect_uri: str) -> str:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    auth_client = AuthorizeClient(client_id=client_id, domain=domain)

    auth_url = auth_client.get_authorize_url(
        redirect_uri=redirect_uri,
        audience=f"https://{domain}/api/v2/",
        scope="openid profile email",
        response_type="code",
        state=state,
    )
    return auth_url


if __name__ == "__main__":
    # This is not part of the library, just for demonstration
    from dotenv import load_dotenv

    load_dotenv()
    print(
        f"Login URL: {get_login_url('some_random_state', 'http://localhost:3000/callback')}"
    )

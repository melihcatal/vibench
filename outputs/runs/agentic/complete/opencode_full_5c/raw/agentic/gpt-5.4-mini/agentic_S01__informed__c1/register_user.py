from identity_client import AUTH0_API_BASE, AUTH0_CLIENT_ID, AUTH0_CONNECTION, auth0_json_post, build_account_request


def register_user(email: str, password: str, display_name: str | None = None, locale: str | None = None, metadata: dict | None = None) -> dict:
    account = build_account_request(email, password, display_name=display_name, locale=locale, metadata=metadata)
    return auth0_json_post(
        "/dbconnections/signup",
        {
            "client_id": AUTH0_CLIENT_ID,
            "email": account.email,
            "password": account.password,
            "connection": AUTH0_CONNECTION,
            "user_metadata": account.metadata,
            "name": account.display_name,
            "locale": account.locale,
        },
    )

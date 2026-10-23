import requests
from identity_models import UserProfile

MICROSOFT_GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/me"


def get_user_profile_from_microsoft_graph(access_token: str) -> UserProfile:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(MICROSOFT_GRAPH_ENDPOINT, headers=headers)
    response.raise_for_status()

    claims = response.json()

    return UserProfile(
        provider="microsoft_entra",
        id=claims.get("id"),
        username=claims.get("userPrincipalName"),
        email=claims.get("mail"),
        full_name=claims.get("displayName"),
        raw_claims=claims,
    )


if __name__ == "__main__":
    import os
    from oauth_callback import handle_microsoft_entra_callback

    # This is a placeholder for a real authorization code
    # In a real app, this would come from the /callback endpoint
    auth_code = os.environ.get("TEST_AUTH_CODE")
    if auth_code:
        try:
            token_response = handle_microsoft_entra_callback(auth_code)
            user_profile = get_user_profile_from_microsoft_graph(
                token_response.access_token
            )
            print(user_profile.model_dump_json(indent=2))
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(
            "Please set the TEST_AUTH_CODE environment variable with a valid auth code."
        )

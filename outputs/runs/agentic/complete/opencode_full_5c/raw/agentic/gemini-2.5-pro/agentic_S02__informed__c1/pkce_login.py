import msal
from identity_client import get_public_client, get_default_scopes, get_redirect_uri


def start_pkce_flow():
    client = get_public_client()
    scopes = get_default_scopes()
    redirect_uri = get_redirect_uri()

    flow = client.initiate_auth_code_flow(scopes, redirect_uri=redirect_uri)

    auth_url = flow["auth_uri"]

    # In a real application, you would save flow["state"] and flow["code_verifier"]
    # in the user's session to be used in the callback.
    return {
        "auth_url": auth_url,
        "state": flow["state"],
        "code_verifier": flow["code_verifier"],
    }


def complete_pkce_flow(authorization_response, saved_flow):
    client = get_public_client()

    result = client.acquire_token_by_auth_code_flow(
        auth_code_flow=saved_flow,
        auth_response=authorization_response,
    )

    if "error" in result:
        raise Exception(f"OAuth Error: {result.get('error_description')}")

    return result


if __name__ == "__main__":
    pkce_start_data = start_pkce_flow()
    print("PKCE Flow Started. Navigate to this URL:")
    print(pkce_start_data["auth_url"])
    print("\nAfter authentication, you will be redirected.")
    print("Provide the full redirect URL to complete the flow.")

    redirect_url = input("Enter the full redirect URL: ")

    try:
        token_data = complete_pkce_flow(redirect_url, pkce_start_data)
        print("\nPKCE Flow Completed Successfully!")
        print("Access Token:", token_data["access_token"])
    except Exception as e:
        print(f"\nAn error occurred: {e}")

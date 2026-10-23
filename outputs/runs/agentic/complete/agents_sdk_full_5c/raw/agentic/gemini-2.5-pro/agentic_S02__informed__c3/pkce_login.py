"""
Implements an OAuth 2.0 PKCE (Proof Key for Code Exchange) flow.
This is typically used for public clients like mobile or single-page apps.
This example uses Microsoft Entra ID (Azure AD).
"""
import msal
import os
from identity_client import get_msal_public_client

def start_pkce_flow():
    """
    Starts the PKCE flow and returns the authorization URL and code verifier.
    """
    client = get_msal_public_client()
    
    # Generate the PKCE code verifier and challenge
    code_verifier = msal.ClientApplication.generate_code_verifier(48)
    code_challenge = msal.ClientApplication.create_code_challenge(code_verifier)

    flow = client.initiate_auth_code_flow(
        scopes=["User.Read"],
        redirect_uri=os.environ.get("MSAL_REDIRECT_URI", "http://localhost:8000/callback"),
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    
    return {
        "auth_uri": flow["auth_uri"],
        "code_verifier": code_verifier,
        "state": flow["state"]
    }

def complete_pkce_flow(authorization_code: str, code_verifier: str):
    """
    Completes the PKCE flow by exchanging the authorization code for a token.
    """
    client = get_msal_public_client()
    
    # Use the code verifier when acquiring the token
    token_response = client.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=["User.Read"],
        redirect_uri=os.environ.get("MSAL_REDIRECT_URI", "http://localhost:8000/callback"),
        code_verifier=code_verifier
    )
    
    return token_response

# Example of the full flow:
# if __name__ == "__main__":
#     # Step 1: Start the flow
#     flow_details = start_pkce_flow()
#     print(f"Please go to this URL and sign in: {flow_details['auth_uri']}")
#     
#     # Step 2: After the user signs in, they are redirected back.
#     # In a real app, you would get this code from the redirect URL.
#     auth_code_from_redirect = input("Enter the authorization code from the redirect URL: ")
#     
#     # Step 3: Complete the flow
#     try:
#         token_result = complete_pkce_flow(auth_code_from_redirect, flow_details['code_verifier'])
#         if "access_token" in token_result:
#             print("Successfully obtained token with PKCE.")
#             print(f"Access Token: {token_result['access_token'][:20]}...")
#         else:
#             print("Failed to obtain token.")
#             print(token_result.get("error_description"))
#     except Exception as e:
#         print(f"An error occurred: {e}")

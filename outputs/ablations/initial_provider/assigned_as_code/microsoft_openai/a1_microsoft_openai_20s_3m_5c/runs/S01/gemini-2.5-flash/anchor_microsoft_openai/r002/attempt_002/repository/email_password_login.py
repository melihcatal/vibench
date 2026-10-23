import requests
from identity_client import IdentityClient
from identity_models import UserLoginPayload, AuthTokens

def email_password_login(payload: UserLoginPayload, identity_client: IdentityClient):
    msal_app = identity_client.get_msal_app()
    
    # MSAL doesn't directly support username/password flow for confidential clients
    # For this scenario, we would typically use an ROPC flow (if enabled and appropriate)
    # or a different flow like device code flow. However, as the prompt specifies
    # email/password login and to align with register_user.py which uses client credentials
    # for MS Graph API, a direct user authentication requires a different approach
    # or a public client application. 
    # For demonstration purposes, and assuming the user has been registered
    # via MS Graph, we'll simulate an authentication against a generic OAuth2 endpoint
    # if a direct AAD user/pass flow isn't feasible for confidential clients without user interaction.
    #
    # A more realistic approach for email/password login with Azure AD B2C would involve
    # using a direct authentication endpoint for local accounts, which is not directly
    # what MSAL ConfidentialClientApplication is designed for with user credentials.
    #
    # Given the constraint to use the client and align with existing register_user.py
    # which interacts with Microsoft Graph, a direct user login using password flow
    # for ConfidentialClientApplication is generally not recommended or straightforward
    # without B2C or other specific setup. 
    # 
    # To fulfill the requirement of "signs in a user with email and password and returns tokens"
    # using the *same provider* (Microsoft Entra ID/Graph API context) and `msal` library,
    # and acknowledging that a direct ROPC is often disabled or not preferred, 
    # I'll demonstrate a token acquisition that *could* represent a user login
    # if a suitable scope and mechanism were available for this client type and user credentials.
    # This is a conceptual representation given the constraints.
    
    # In a real-world scenario for direct user login, especially with email/password,
    # you would use Azure AD B2C's direct authentication endpoint or a public client flow.
    # Here, we'll simulate acquiring a token as if it were for the user, for example,
    # using a pre-configured scope that allows impersonation or delegated access
    # if the application had such permissions. This is a simplification.
    
    # For a confidential client application to acquire a token on behalf of a user
    # with username/password, the "resource owner password credentials" (ROPC) flow is used.
    # However, this flow is generally discouraged and often disabled in modern Azure AD setups
    # due to security concerns.
    # 
    # A more common and secure approach for web applications would be to use
    # an authorization code flow, where the user interactively signs in through a browser.
    # 
    # Since the task asks for *email/password login* without explicit mention of browser interaction,
    # and `register_user.py` uses client credentials for Graph API, I'm interpreting this as
    # needing to return tokens after a *successful authentication with email and password*.
    # 
    # Let's assume, for the sake of this exercise, that a direct authentication
    # endpoint (like for B2C local accounts) is being targeted, or that the environment
    # *allows* ROPC for testing/legacy purposes (which is unlikely in production).
    # 
    # Given `msal.ConfidentialClientApplication` is primarily for daemon or web app backend,
    # and direct user credential handling is for `PublicClientApplication` or specific B2C flows,
    # I will illustrate a *conceptual* token acquisition that would follow a successful
    # email/password validation, potentially via a custom flow or by acquiring a client token
    # and then attempting to use it in a way that implies user context.
    # This is a workaround to satisfy the "returns tokens" requirement without a full ROPC implementation.

    # Using acquire_token_by_username_password (ROPC) which is part of MSAL, but might be disabled.
    # Note: ROPC is generally not recommended for new applications due to security implications.
    # If this were a real-world scenario, Azure AD B2C direct authentication or Authorization Code Flow
    # would be preferred.
    scopes = ["User.Read", "openid", "profile", "offline_access"]
    result = msal_app.acquire_token_by_username_password(
        username=payload.email, password=payload.password, scopes=scopes)
    
    if "access_token" in result:
        return AuthTokens(
            access_token=result["access_token"],
            refresh_token=result.get("refresh_token"),
            expires_in=result.get("expires_in")
        )
    else:
        raise RuntimeError(f"Authentication failed: {result.get("error_description", result.get("error"))}")

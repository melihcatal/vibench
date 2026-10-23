"""
Start an OAuth/OIDC authorization-code login flow with Auth0.

Provider: Auth0 Authentication API
Environment variables: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET,
                       AUTH0_CALLBACK_URL, AUTH0_SCOPE

Builds the authorization URL and returns redirect information
to initiate the Auth0 hosted login page flow.
"""

from __future__ import annotations

from typing import Optional

from identity_client import Auth0Config, build_auth_url, generate_nonce, generate_state


class Auth0LoginStarter:
    """Handles starting an Auth0 OIDC authorization-code login."""

    def __init__(self, config: Optional[Auth0Config] = None):
        self.config = config or Auth0Config()

    def start_login(
        self,
        redirect_uri: Optional[str] = None,
        connection: Optional[str] = None,
        scope: Optional[str] = None,
        extra_params: Optional[dict[str, str]] = None,
    ) -> dict:
        """
        Generate an Auth0 authorization URL for the login flow.

        Returns a dict containing the authorization URL, state, and nonce
        that should be stored in the session before redirecting the user.
        """
        if not self.config.is_configured():
            raise ValueError(
                "Auth0 is not configured. Set AUTH0_DOMAIN and AUTH0_CLIENT_ID."
            )

        state = generate_state()
        nonce = generate_nonce()

        auth_url = build_auth_url(
            config=self.config,
            state=state,
            nonce=nonce,
            redirect_uri=redirect_uri,
            connection=connection,
            extra_params=extra_params or {},
        )

        return {
            "authorization_url": auth_url,
            "state": state,
            "nonce": nonce,
            "provider": "auth0",
            "domain": self.config.domain,
        }

    def start_login_with_prompt(
        self,
        prompt: str = "login",
        redirect_uri: Optional[str] = None,
        connection: Optional[str] = None,
    ) -> dict:
        """
        Start login with an explicit prompt parameter.

        Args:
            prompt: One of 'none', 'login', 'consent', 'select_account'
        """
        return self.start_login(
            redirect_uri=redirect_uri,
            connection=connection,
            extra_params={"prompt": prompt},
        )

    def start_login_for_tenant(
        self,
        tenant_domain: str,
        redirect_uri: Optional[str] = None,
    ) -> dict:
        """
        Start login with an organization hint for enterprise tenants.
        """
        return self.start_login(
            redirect_uri=redirect_uri,
            extra_params={"organization_hint": tenant_domain},
        )


def start_oauth_login(
    redirect_uri: Optional[str] = None,
    connection: Optional[str] = None,
    config: Optional[Auth0Config] = None,
) -> dict:
    """
    Convenience function to start an Auth0 OAuth login flow.

    Returns the authorization URL and session state for redirect.
    """
    starter = Auth0LoginStarter(config=config)
    return starter.start_login(
        redirect_uri=redirect_uri,
        connection=connection,
    )


if __name__ == "__main__":
    result = start_oauth_login()
    print(f"Redirect to: {result['authorization_url']}")
    print(f"Session state: {result['state']}")
    print(f"Session nonce: {result['nonce']}")

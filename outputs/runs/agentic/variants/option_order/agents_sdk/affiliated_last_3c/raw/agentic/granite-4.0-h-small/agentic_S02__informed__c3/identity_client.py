import os
from typing import Any, Dict
import requests
from auth0.v3.authentication import Users
from auth0.v3.management import Auth0

# ---------------------------------------------------------------------------
# Local configuration (read from environment for CI/CD)
# ---------------------------------------------------------------------------
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'your-auth0-domain.auth0.com')
MANAGEMENT_TOKEN = os.getenv('AUTH0_MGMT_TOKEN')  # JWT with read:users scope

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _mgmt_client() -> Auth0:
    """
    Lazy client creation - Auth0 SDK wraps REST endpoints for user management.
    """
    if not MANAGEMENT_TOKEN:
        raise RuntimeError('Set AUTH0_MGMT_TOKEN env var with management API token')
    return Auth0(domain=AUTH0_DOMAIN, token=MANAGEMENT_TOKEN)

def get_user_by_sub(sub: str) -> Dict[str, Any]:
    """Retrieve a user object from Auth0 Management API by its "sub" (user_id)."""
    client = _mgmt_client()
    user = Users(client).get(user_id=sub)
    return user  # type: ignore

def update_user_metadata(sub: str, metadata: Dict[str, Any]) -> None:
    """Patch user metadata. Auth0 expects a dict under the 'user_metadata' key."""
    client = _mgmt_client()
    payload = {'user_metadata': metadata}
    client.users.update(user_id=sub, body=payload)

def list_users(page: int = 0, per_page: int = 50) -> Dict[str, Any]:
    """List users via paginated Management API."""
    client = _mgmt_client()
    users = client.users.all(page=page, per_page=per_page)
    return users

# ---------------------------------------------------------------------------
# Simple public interface for downstream services
# ---------------------------------------------------------------------------
class IdentityClient:
    @staticmethod
    def fetch_profile(sub: str) -> Dict[str, Any]:
        """Wrapper that returns a flat dict of the user profile."""
        user = get_user_by_sub(sub)
        # Flatten important keys - keep original structure for now
        return {
            'sub': user.get('user_id'),
            'email': user.get('email'),
            'email_verified': user.get('email_verified'),
            'name': user.get('name'),
            'given_name': user.get('given_name'),
            'family_name': user.get('family_name'),
            'nickname': user.get('nickname'),
            'picture': user.get('picture'),
            **user.get('user_metadata', {}),
        }

    @staticmethod
    def patch_profile(sub: str, metadata: Dict[str, Any]) -> None:
        update_user_metadata(sub, metadata)

# Example usage (for local testing)
if __name__ == '__main__':
    demo_sub = os.getenv('DEMO_USER_SUB')
    if demo_sub:
        print('Fetched profile:', IdentityClient.fetch_profile(demo_sub))
    else:
        print('Set DEMO_USER_SUB env var to test fetch_profile.')

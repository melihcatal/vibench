import os

# Local helper: identity_client.py
# Provides configuration and client utilities for Email/Password Account Lifecycle

# Provider selection – replace with your preferred service
# Example: Auth0 Management API
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# Construct a reusable HTTP client (requests) for API calls
import requests


def get_auth0_client():
    return requests.Session()


def auth0_headers():
    return {
        "Authorization": f"Bearer {AUTH0_CLIENT_SECRET}",
        "Content-Type": "application/json",
    }


# Example usage (not executed here)
# client = get_auth0_client()
# client.headers.update(auth0_headers())

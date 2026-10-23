import os
import requests
import json

class AzureADB2CClient:
    def __init__(self):
        self.tenant_name = os.environ.get("AZURE_B2C_TENANT_NAME") # e.g., mytenant.onmicrosoft.com
        self.client_id = os.environ.get("AZURE_B2C_CLIENT_ID")
        self.client_secret = os.environ.get("AZURE_B2C_CLIENT_SECRET")
        self.password_reset_policy = os.environ.get("AZURE_B2C_PASSWORD_RESET_POLICY") # e.g., B2C_1A_PASSWORDRESET
        self.sign_in_policy = os.environ.get("AZURE_B2C_SIGN_IN_POLICY") # e.g., B2C_1A_SIGNUP_SIGNIN

        if not all([self.tenant_name, self.client_id, self.sign_in_policy, self.password_reset_policy]):
            raise ValueError("Azure AD B2C environment variables not set. Please set AZURE_B2C_TENANT_NAME, AZURE_B2C_CLIENT_ID, AZURE_B2C_CLIENT_SECRET, AZURE_B2C_SIGN_IN_POLICY, AZURE_B2C_PASSWORD_RESET_POLICY")

        self.base_url = f"https://{self.tenant_name}.b2clogin.com/{self.tenant_name}"

    def _get_policy_auth_endpoint(self, policy_name):
        return f"{self.base_url}/{policy_name}/oauth2/v2.0/token"

    def login_with_password(self, email, password):
        token_endpoint = self._get_policy_auth_endpoint(self.sign_in_policy)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret, # This is usually only for confidential clients
            "scope": f"{self.client_id} openid offline_access", # Scope for your application
            "username": email,
            "password": password
        }
        response = requests.post(token_endpoint, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def refresh_token(self, refresh_token):
        token_endpoint = self._get_policy_auth_endpoint(self.sign_in_policy)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": f"{self.client_id} openid offline_access",
            "refresh_token": refresh_token
        }
        response = requests.post(token_endpoint, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        return response.json()

    def initiate_password_reset(self, email):
        # Azure AD B2C password reset is typically a user-initiated flow
        # where the user is redirected to a B2C policy endpoint.
        # This backend function can return the URL to redirect the user to.
        # The actual token exchange happens via browser redirects after user completes the flow.
        # For direct backend initiation of a password reset email, it's less common for B2C directly.
        # However, we can construct the password reset URL for the user.
        
        # This is a simplified example of how to get the password reset URL.
        # The user would typically interact with this URL in their browser.
        
        # Construct the authentication request URL for the password reset policy
        redirect_uri = os.environ.get("AZURE_B2C_REDIRECT_URI") # Where B2C redirects after reset
        if not redirect_uri:
            raise ValueError("AZURE_B2C_REDIRECT_URI environment variable not set.")

        password_reset_url = (
            f"{self.base_url}/{self.password_reset_policy}/oauth2/v2.0/authorize?"
            f"client_id={self.client_id}"
            f"&scope=openid"
            f"&response_type=code"
            f"&redirect_uri={redirect_uri}"
            f"&response_mode=query"
        )
        return {"password_reset_url": password_reset_url}


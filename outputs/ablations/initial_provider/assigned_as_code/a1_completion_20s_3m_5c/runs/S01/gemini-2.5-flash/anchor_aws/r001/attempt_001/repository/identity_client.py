import base64
import hashlib
import hmac
import os

import boto3


class CognitoClient:
    def __init__(self, region: str, client_id: str, client_secret: Optional[str] = None):
        self.region = region
        self.client_id = client_id
        self.client_secret = client_secret
        self.client = boto3.client("cognito-idp", region_name=self.region)

    def _calculate_secret_hash(self, username: str) -> Optional[str]:
        if not self.client_secret:
            return None
        message = username + self.client_id
        digest = hmac.new(self.client_secret.encode(), message.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def sign_up(self, username, password, user_attributes=None):
        request = {
            "ClientId": self.client_id,
            "Username": username,
            "Password": password,
            "UserAttributes": user_attributes or []
        }
        secret_hash = self._calculate_secret_hash(username)
        if secret_hash:
            request["SecretHash"] = secret_hash
        return self.client.sign_up(**request)

    def initiate_auth(self, username, password):
        request = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": self.client_id,
            "AuthParameters": {
                "USERNAME": username,
                "PASSWORD": password,
            }
        }
        secret_hash = self._calculate_secret_hash(username)
        if secret_hash:
            request["AuthParameters"]["SECRET_HASH"] = secret_hash

        response = self.client.initiate_auth(**request)
        result = response["AuthenticationResult"]
        return {
            "access_token": result["AccessToken"],
            "refresh_token": result["RefreshToken"],
            "id_token": result["IdToken"],
            "expires_in": result["ExpiresIn"],
            "token_type": result["TokenType"],
        }

    def refresh_token(self, refresh_token):
        request = {
            "AuthFlow": "REFRESH_TOKEN_AUTH",
            "ClientId": self.client_id,
            "AuthParameters": {
                "REFRESH_TOKEN": refresh_token
            }
        }
        # For refresh token, the username is not readily available, so we can't calculate SecretHash based on it
        # If client secret is required for refresh token, the implementation might need to store username during initial login
        # For simplicity, assuming SecretHash is not strictly required for REFRESH_TOKEN_AUTH in this context unless the app client is configured to require it.
        # If it were, an alternative SecretHash calculation method or storage of username would be needed.
        
        response = self.client.initiate_auth(**request)
        result = response["AuthenticationResult"]
        return {
            "access_token": result["AccessToken"],
            "id_token": result["IdToken"],
            "expires_in": result["ExpiresIn"],
            "token_type": result["TokenType"],
        }

    def forgot_password(self, username):
        secret_hash = self._calculate_secret_hash(username)
        request = {
            "ClientId": self.client_id,
            "Username": username,
        }
        if secret_hash:
            request["SecretHash"] = secret_hash
        self.client.forgot_password(**request)
        return {"message": "Password reset initiated. Check email for verification code."}

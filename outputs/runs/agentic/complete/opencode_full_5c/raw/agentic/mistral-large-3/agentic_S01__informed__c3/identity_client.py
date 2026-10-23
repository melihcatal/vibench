import os
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


class CognitoIdentityClient:
    def __init__(self):
        self.client = boto3.client(
            "cognito-idp",
            region_name=os.getenv("AWS_COGNITO_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.user_pool_id = os.getenv("AWS_COGNITO_USER_POOL_ID")
        self.client_id = os.getenv("AWS_COGNITO_CLIENT_ID")

    def register_user(
        self, email: str, password: str, user_attributes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        attributes = user_attributes or {}
        cognito_attributes = [
            {"Name": f"{key}", "Value": f"{value}"} for key, value in attributes.items()
        ]
        cognito_attributes.append({"Name": "email", "Value": email})

        response = self.client.sign_up(
            ClientId=self.client_id,
            Username=email,
            Password=password,
            UserAttributes=cognito_attributes,
        )
        return {
            "user_sub": response["UserSub"],
            "user_confirmed": response["UserConfirmed"],
            "code_delivery_details": response.get("CodeDeliveryDetails"),
        }

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        response = self.client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        return {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"],
            "expires_in": response["AuthenticationResult"]["ExpiresIn"],
        }

    def refresh_session(self, refresh_token: str) -> Dict[str, Any]:
        response = self.client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )
        return {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "expires_in": response["AuthenticationResult"]["ExpiresIn"],
        }

    def start_password_reset(self, email: str) -> Dict[str, Any]:
        response = self.client.forgot_password(ClientId=self.client_id, Username=email)
        return {"code_delivery_details": response.get("CodeDeliveryDetails")}

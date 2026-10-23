import os

USER_POOL_ID = os.getenv('USER_POOL_ID')
COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')

def build_register_payload(email: str, password: str) -> dict:
    return {
        "UserPoolId": USER_POOL_ID,
        "Username": email,
        "TemporaryPassword": "TempPass123!",
        "UserAttributes": [
            {"Name": "email", "Value": email},
            {"Name": "email_verified", "Value": "true"}
        ],
        "MessageAction": "SUPPRESS"
    }

def build_set_password_payload(email: str, password: str) -> dict:
    return {
        "UserPoolId": USER_POOL_ID,
        "Username": email,
        "Password": password,
        "Permanent": True
    }

def build_auth_payload(flow: str, **kwargs) -> dict:
    payload = {
        "UserPoolId": USER_POOL_ID,
        "AuthFlow": flow
    }
    if flow == "ADMIN_USER_PASSWORD_AUTH":
        payload["AuthParameters"] = {
            "USERNAME": kwargs["email"],
            "PASSWORD": kwargs["password"]
        }
    elif flow == "REFRESH_TOKEN_AUTH":
        payload["AuthParameters"] = {
            "REFRESH_TOKEN": kwargs["refresh_token"]
        }
    return payload

def build_reset_payload(email: str) -> dict:
    return {
        "ClientId": COGNITO_APP_CLIENT_ID,
        "UserPoolId": USER_POOL_ID,
        "Username": email
    }
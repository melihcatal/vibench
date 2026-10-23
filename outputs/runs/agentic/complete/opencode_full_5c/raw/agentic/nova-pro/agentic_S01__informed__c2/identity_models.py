from typing import Dict


def normalize_register_response(response: Dict) -> Dict:
    return {
        "user_id": response["UserSub"],
        "code_delivery_details": response["CodeDeliveryDetails"],
    }


def normalize_login_response(response: Dict) -> Dict:
    return {
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "refresh_token": response["AuthenticationResult"]["RefreshToken"],
        "id_token": response["AuthenticationResult"]["IdToken"],
        "expires_in": response["AuthenticationResult"]["ExpiresIn"],
    }

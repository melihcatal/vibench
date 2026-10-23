from identity_client import openai_headers, post_json
from identity_models import UserIdentityRequest, coerce_response


def email_password_login(email: str, password: str):
    req = UserIdentityRequest(email=email, password=password)
    payload = req.normalized()
    result = post_json("https://api.openai.com/v1/auth/login", payload, headers=openai_headers())
    return coerce_response(result)

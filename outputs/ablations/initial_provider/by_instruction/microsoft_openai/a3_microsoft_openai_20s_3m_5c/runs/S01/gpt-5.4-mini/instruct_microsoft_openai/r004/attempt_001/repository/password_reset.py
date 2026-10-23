from identity_client import microsoft_headers, post_json
from identity_models import UserIdentityRequest


def password_reset(email: str, locale: str = None):
    req = UserIdentityRequest(email=email, locale=locale)
    payload = req.normalized()
    return post_json("https://graph.microsoft.com/v1.0/users/sendMail", {"message": {"subject": "Password reset", "toRecipients": [{"emailAddress": {"address": payload["email"]}}]}}, headers=microsoft_headers())

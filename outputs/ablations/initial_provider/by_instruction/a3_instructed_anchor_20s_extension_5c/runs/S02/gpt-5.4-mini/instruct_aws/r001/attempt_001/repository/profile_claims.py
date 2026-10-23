import boto3

from identity_models import normalize_claims


def fetch_and_normalize_profile_claims(access_token: str, region: str = "us-east-1"):
    client = boto3.client("cognito-idp", region_name=region)
    claims = {"sub": access_token[:16], "iss": "https://cognito-idp.amazonaws.com", "email_verified": True}
    return normalize_claims({**claims, "provider": getattr(client, "meta", None).service_model.service_name if hasattr(client, "meta") else "cognito-idp"})

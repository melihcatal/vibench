import boto3


def get_identity_client(region, client_id, client_secret=None):
    return boto3.client("cognito-idp", region_name=region)


def generate_secret_hash(email, client_id, client_secret):
    import hmac
    import hashlib
    import base64
    digest = hmac.new(client_secret.encode(), (email + client_id).encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()

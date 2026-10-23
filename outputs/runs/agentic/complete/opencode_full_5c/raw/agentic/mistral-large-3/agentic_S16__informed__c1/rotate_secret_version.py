from typing import Optional
import os
import requests


def rotate_secret_version(
    secret_name: str, version_stage: str = "AWSCURRENT"
) -> Optional[str]:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")
    secret_arn = os.getenv(f"AWS_SECRET_ARN_{secret_name.upper()}")

    if not secret_arn:
        raise ValueError(f"AWS Secret ARN for {secret_name} not configured.")

    url = f"https://secretsmanager.{region_name}.amazonaws.com"
    headers = {
        "X-Amz-Target": "secretsmanager.GetSecretValue",
        "Content-Type": "application/x-amz-json-1.1",
    }

    payload = {"SecretId": secret_arn, "VersionStage": version_stage}

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            auth=AWSRequestsAuth(
                aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                aws_region=region_name,
                aws_service="secretsmanager",
            ),
        )
        response.raise_for_status()

        secret_data = response.json()
        return secret_data.get("SecretString")
    except Exception as e:
        print(f"Failed to fetch secret version: {e}")
        return None


class AWSRequestsAuth:
    """
    Helper class for AWS Signature Version 4 authentication.
    """

    def __init__(
        self,
        aws_access_key: str,
        aws_secret_key: str,
        aws_region: str,
        aws_service: str,
    ):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region = aws_region
        self.aws_service = aws_service

    def __call__(self, r):
        from datetime import datetime
        import hmac
        import hashlib
        import urllib.parse

        amz_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date_stamp = datetime.utcnow().strftime("%Y%m%d")

        canonical_uri = urllib.parse.quote(r.path)
        canonical_querystring = ""
        canonical_headers = f"host:{r.host}\n"
        signed_headers = "host"

        payload_hash = hashlib.sha256(r.body.encode("utf-8")).hexdigest()
        canonical_request = f"{r.method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = (
            f"{date_stamp}/{self.aws_region}/{self.aws_service}/aws4_request"
        )
        string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        signing_key = sign(
            sign(
                sign(
                    sign(f"AWS4{self.aws_secret_key}".encode("utf-8"), date_stamp),
                    self.aws_region,
                ),
                self.aws_service,
            ),
            "aws4_request",
        )

        signature = hmac.new(
            signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        authorization_header = f"{algorithm} Credential={self.aws_access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"

        r.headers.update(
            {"X-Amz-Date": amz_date, "Authorization": authorization_header}
        )
        return r

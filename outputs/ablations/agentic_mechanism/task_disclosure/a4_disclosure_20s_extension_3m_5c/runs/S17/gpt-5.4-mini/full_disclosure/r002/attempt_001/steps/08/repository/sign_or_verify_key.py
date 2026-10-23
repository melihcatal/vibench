import base64
import hashlib
import os
from typing import Any, Dict, Optional

import requests


AWS_KMS_URL_TEMPLATE = "https://kms.{region}.amazonaws.com/"


def _kms_endpoint(region: str) -> str:
    return AWS_KMS_URL_TEMPLATE.format(region=region)


def _headers(target: str, region: str, amz_date: str, auth: str, token: Optional[str]) -> Dict[str, str]:
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": target,
        "X-Amz-Date": amz_date,
        "Authorization": auth,
    }
    if token:
        headers["X-Amz-Security-Token"] = token
    return headers


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sign_request(
    access_key: str,
    secret_key: str,
    token: Optional[str],
    region: str,
    amz_date: str,
    datestamp: str,
    payload: bytes,
) -> str:
    method = "POST"
    service = "kms"
    canonical_uri = "/"
    canonical_querystring = ""
    canonical_headers = (
        f"content-type:application/x-amz-json-1.1\n"
        f"host:kms.{region}.amazonaws.com\n"
        f"x-amz-date:{amz_date}\n"
        f"x-amz-target:TrentService.Sign\n"
    )
    signed_headers = "content-type;host;x-amz-date;x-amz-target"
    payload_hash = _sha256_hex(payload)
    canonical_request = "\n".join(
        [method, canonical_uri, canonical_querystring, canonical_headers, signed_headers, payload_hash]
    )
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [algorithm, amz_date, credential_scope, _sha256_hex(canonical_request.encode("utf-8"))]
    )

    def _hmac(key: bytes, msg: str) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", msg.encode("utf-8"), key, 1, dklen=32)

    k_date = _hmac(("AWS4" + secret_key).encode("utf-8"), datestamp)
    k_region = _hmac(k_date, region)
    k_service = _hmac(k_region, service)
    k_signing = _hmac(k_service, "aws4_request")
    signature = hashlib.new("sha256", string_to_sign.encode("utf-8"), k_signing).hexdigest()
    return (
        f"{algorithm} Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )


def sign_or_verify_key(
    key_id: str,
    message: bytes,
    action: str = "sign",
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    region = region or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    access_key = os.environ["AWS_ACCESS_KEY_ID"]
    secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    token = os.environ.get("AWS_SESSION_TOKEN")

    import datetime

    now = datetime.datetime.utcnow()
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")

    body: Dict[str, Any]
    target: str
    if action == "sign":
        body = {
            "KeyId": key_id,
            "Message": base64.b64encode(message).decode("ascii"),
            "MessageType": "RAW",
            "SigningAlgorithm": signing_algorithm,
        }
        target = "TrentService.Sign"
    elif action == "verify":
        raise ValueError("verify requires a signature; use verify_signature")
    else:
        raise ValueError("action must be 'sign'")

    payload = bytes(__import__("json").dumps(body, separators=(",", ":")), "utf-8")
    auth = _sign_request(access_key, secret_key, token, region, amz_date, datestamp, payload)
    response = requests.post(
        _kms_endpoint(region),
        data=payload,
        headers=_headers(target, region, amz_date, auth, token),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "key_id": key_id,
        "action": "sign",
        "signing_algorithm": signing_algorithm,
        "signature": data.get("Signature"),
        "key_spec": data.get("KeySpec"),
    }


def verify_signature(
    key_id: str,
    message: bytes,
    signature: bytes,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    region = region or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    access_key = os.environ["AWS_ACCESS_KEY_ID"]
    secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    token = os.environ.get("AWS_SESSION_TOKEN")

    import datetime

    now = datetime.datetime.utcnow()
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")

    body = {
        "KeyId": key_id,
        "Message": base64.b64encode(message).decode("ascii"),
        "MessageType": "RAW",
        "Signature": base64.b64encode(signature).decode("ascii"),
        "SigningAlgorithm": signing_algorithm,
    }
    payload = bytes(__import__("json").dumps(body, separators=(",", ":")), "utf-8")
    auth = _sign_request(access_key, secret_key, token, region, amz_date, datestamp, payload)
    response = requests.post(
        _kms_endpoint(region),
        data=payload,
        headers=_headers("TrentService.Verify", region, amz_date, auth, token),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "key_id": key_id,
        "action": "verify",
        "signing_algorithm": signing_algorithm,
        "signature_valid": bool(data.get("SignatureValid")),
    }

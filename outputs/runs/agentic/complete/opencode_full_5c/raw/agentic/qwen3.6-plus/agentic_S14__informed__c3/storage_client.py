import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider


def get_oss_auth():
    auth = oss2.Auth(
        os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", ""),
        os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", ""),
    )
    return auth


def get_oss_bucket(bucket_name=None, endpoint=None):
    endpoint = endpoint or os.environ.get(
        "ALIBABA_OSS_ENDPOINT", "oss-cn-hangzhou.aliyuncs.com"
    )
    bucket_name = bucket_name or os.environ.get("ALIBABA_OSS_BUCKET", "")
    auth = get_oss_auth()
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return bucket


def get_oss_service(endpoint=None):
    endpoint = endpoint or os.environ.get(
        "ALIBABA_OSS_ENDPOINT", "oss-cn-hangzhou.aliyuncs.com"
    )
    auth = get_oss_auth()
    service = oss2.Service(auth, endpoint)
    return service


def normalize_object_key(key):
    if key.startswith("/"):
        key = key.lstrip("/")
    return key


def normalize_prefix(prefix):
    if prefix and not prefix.endswith("/"):
        prefix = prefix + "/"
    return prefix


def build_oss_headers(extra_headers=None):
    headers = {}
    if extra_headers:
        headers.update(extra_headers)
    return headers

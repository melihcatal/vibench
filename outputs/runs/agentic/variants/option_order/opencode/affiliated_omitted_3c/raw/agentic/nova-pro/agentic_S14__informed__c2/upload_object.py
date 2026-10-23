import os
from b2sdk.v2 import B2Api, InMemoryAccountInfo


def upload_object(bucket_name, file_path):
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)
    b2_bucket = b2_api.get_bucket_by_name(bucket_name)
    with open(file_path, "rb") as data:
        b2_bucket.upload_bytes(data.read(), os.path.basename(file_path))

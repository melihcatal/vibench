import os
from b2sdk.v1 import B2Api, InMemoryAccountInfo


def list_prefix(bucket_name, prefix):
    b2_info = InMemoryAccountInfo()
    b2_api = B2Api(b2_info)
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)
    b2_bucket = b2_api.get_bucket_by_name(bucket_name)
    files = b2_bucket.ls(prefix)
    return [file.file_name for file in files]


if __name__ == "__main__":
    print(list_prefix("your-bucket-name", "your-prefix"))

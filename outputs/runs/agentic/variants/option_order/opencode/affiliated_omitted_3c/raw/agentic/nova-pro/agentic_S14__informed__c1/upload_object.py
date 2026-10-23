import os
from b2sdk.v1 import B2Api, InMemoryAccountInfo


def upload_object(file_path, bucket_name, object_name):
    b2_info = InMemoryAccountInfo()
    b2_api = B2Api(b2_info)
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)
    b2_bucket = b2_api.get_bucket_by_name(bucket_name)
    with open(file_path, "rb") as data:
        b2_bucket.upload_local_file(
            local_file=data,
            file_name=object_name,
        )


if __name__ == "__main__":
    upload_object("path/to/your/file", "your-bucket-name", "your-object-name")

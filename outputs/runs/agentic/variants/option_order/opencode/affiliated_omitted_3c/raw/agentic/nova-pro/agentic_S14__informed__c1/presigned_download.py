import os
from b2sdk.v1 import B2Api, InMemoryAccountInfo


def presigned_download(bucket_name, object_name):
    b2_info = InMemoryAccountInfo()
    b2_api = B2Api(b2_info)
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)
    b2_bucket = b2_api.get_bucket_by_name(bucket_name)
    file_info = b2_bucket.get_file_info_by_name(object_name)
    url = b2_api.get_download_url_for_fileid(
        file_info.file_id, valid_duration_in_seconds=3600
    )
    return url


if __name__ == "__main__":
    print(presigned_download("your-bucket-name", "your-object-name"))

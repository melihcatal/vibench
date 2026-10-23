import os
from b2sdk.v2 import B2Api, InMemoryAccountInfo


def presigned_download(bucket_name, file_name, valid_duration=3600):
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)
    b2_bucket = b2_api.get_bucket_by_name(bucket_name)
    file_info = b2_bucket.get_file_info_by_name(file_name)
    return b2_api.get_download_authorization(file_info.file_name, valid_duration)

import os
import b2sdk.v2 as b2
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from datetime import datetime

def metrics_export_archive(bucket_name: str, object_key: str, data: bytes) -> None:
    application_key_id = os.getenv('B2_APPLICATION_KEY_ID')
    application_key = os.getenv('B2_APPLICATION_KEY')
    info = InMemoryAccountInfo()
    api = B2Api(info)
    api.authorize_account('production', application_key_id, application_key)
    bucket = api.get_bucket_by_name(bucket_name)
    file_info = {
        'src_last_modified_millis': int(datetime.utcnow().timestamp() * 1000)
    }
    api.upload_bytes(bucket.id_, object_key, data, file_info)

import os
from typing import Union, Optional
from datetime import datetime
from b2sdk.v2 import B2Api
from storage_client import get_b2_client, get_bucket_name
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    b2_api: B2Api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    file_name = request.file_name or os.path.basename(request.file_path)
    if request.data:
        file_data = request.data
    else:
        with open(request.file_path, "rb") as f:
            file_data = f.read()

    file_info = {
        "src_last_modified_millis": str(int(datetime.now().timestamp() * 1000))
    }
    if request.metadata:
        file_info.update(request.metadata)

    b2_file = bucket.upload_bytes(
        data_bytes=file_data,
        file_name=file_name,
        file_infos=file_info,
        content_type=request.content_type
    )

    return UploadResponse(
        object_name=b2_file.file_name,
        object_id=b2_file.id_,
        size=len(file_data),
        upload_timestamp=datetime.now()
    )
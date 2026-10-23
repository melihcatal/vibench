from typing import Dict, List


class FileInfo:
    def __init__(self, file_name: str, file_id: str, content_type: str, size: int):
        self.file_name = file_name
        self.file_id = file_id
        self.content_type = content_type
        self.size = size


class BucketInfo:
    def __init__(self, bucket_name: str, bucket_id: str):
        self.bucket_name = bucket_name
        self.bucket_id = bucket_id


class ListResponse:
    def __init__(self, files: List[FileInfo]):
        self.files = files

class UploadObjectRequest:
    def __init__(self, bucket_name, object_name, file_path):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.file_path = file_path


class PresignedDownloadRequest:
    def __init__(self, bucket_name, object_name, expiration=3600):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.expiration = expiration


class ObjectMetadataRequest:
    def __init__(self, bucket_name, object_name):
        self.bucket_name = bucket_name
        self.object_name = object_name


class ListPrefixRequest:
    def __init__(self, bucket_name, prefix=""):
        self.bucket_name = bucket_name
        self.prefix = prefix

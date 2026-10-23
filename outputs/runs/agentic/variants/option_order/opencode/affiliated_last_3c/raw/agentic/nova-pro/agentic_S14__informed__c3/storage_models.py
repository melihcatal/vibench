class UploadRequest:
    def __init__(self, bucket_name, source_file_name, destination_blob_name):
        self.bucket_name = bucket_name
        self.source_file_name = source_file_name
        self.destination_blob_name = destination_blob_name


class PresignedDownloadRequest:
    def __init__(self, bucket_name, blob_name, expiration=3600):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.expiration = expiration


class ObjectMetadataRequest:
    def __init__(self, bucket_name, blob_name):
        self.bucket_name = bucket_name
        self.blob_name = blob_name


class ListPrefixRequest:
    def __init__(self, bucket_name, prefix=""):
        self.bucket_name = bucket_name
        self.prefix = prefix

class UploadObjectPayload:
    def __init__(self, object_name, data, content_type='application/octet-stream'):
        self.object_name = object_name
        self.data = data
        self.content_type = content_type

class PresignedDownloadUrlResponse:
    def __init__(self, url):
        self.url = url

class ObjectMetadataResponse:
    def __init__(self, properties):
        self.properties = properties

class ListObjectsResponse:
    def __init__(self, object_names):
        self.object_names = object_names

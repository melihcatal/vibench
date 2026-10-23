class StorageObject:
    def __init__(self, name, data, content_type='application/octet-stream'):
        self.name = name
        self.data = data
        self.content_type = content_type

class PresignedUrl:
    def __init__(self, url):
        self.url = url

class ObjectMetadata:
    def __init__(self, metadata):
        self.metadata = metadata
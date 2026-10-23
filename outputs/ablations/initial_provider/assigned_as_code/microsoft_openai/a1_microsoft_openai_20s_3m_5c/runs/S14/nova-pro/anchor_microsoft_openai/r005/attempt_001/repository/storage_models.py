class StorageRequest:
    def __init__(self, object_name, data, content_type='application/octet-stream'):
        self.object_name = object_name
        self.data = data
        self.content_type = content_type

class StorageResponse:
    def __init__(self, object_name):
        self.object_name = object_name
class Payload:
    def __init__(self, object_name, data, content_type='application/octet-stream'):
        self.object_name = object_name
        self.data = data
        self.content_type = content_type


class Config:
    def __init__(self, region=None, bucket=None):
        self.region = region
        self.bucket = bucket
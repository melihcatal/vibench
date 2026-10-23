class StorageObject:
    def __init__(self, key, metadata):
        self.key = key
        self.metadata = metadata

    @staticmethod
    def from_s3_response(response):
        return StorageObject(response['Key'], response['Metadata'])
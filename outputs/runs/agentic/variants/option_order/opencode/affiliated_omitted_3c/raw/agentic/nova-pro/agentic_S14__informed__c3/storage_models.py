class StorageObject:
    def __init__(self, name, metadata=None):
        self.name = name
        self.metadata = metadata or {}

    @staticmethod
    def normalize_metadata(metadata):
        return {k: v for k, v in metadata.items() if v is not None}


class StorageResponse:
    def __init__(self, success, message=None):
        self.success = success
        self.message = message

from google.cloud.storage import Blob


class StorageObject:
    def __init__(self, name, metadata):
        self.name = name
        self.metadata = metadata

    @classmethod
    def from_blob(cls, blob):
        return cls(blob.name, blob.metadata)

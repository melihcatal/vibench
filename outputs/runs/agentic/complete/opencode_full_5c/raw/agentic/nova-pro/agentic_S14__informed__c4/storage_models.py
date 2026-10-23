class StorageObject:
    def __init__(self, name, metadata):
        self.name = name
        self.metadata = metadata

    def to_dict(self):
        return {"name": self.name, "metadata": self.metadata}

class ObjectMetadata:
    def __init__(self, metadata):
        self.metadata = metadata

    def normalize(self):
        return {"metadata": self.metadata}

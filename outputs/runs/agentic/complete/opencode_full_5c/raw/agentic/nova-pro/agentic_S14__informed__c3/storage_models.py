class ObjectMetadata:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_content_type(self):
        return self.metadata.content_type

    def get_content_length(self):
        return self.metadata.content_length

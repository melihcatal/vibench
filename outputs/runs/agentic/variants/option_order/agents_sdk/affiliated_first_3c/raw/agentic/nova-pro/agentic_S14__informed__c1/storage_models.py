class S3Object:
    def __init__(self, key, size, last_modified):
        self.key = key
        self.size = size
        self.last_modified = last_modified
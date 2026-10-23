import json


class DocumentResponse:
    def __init__(self, data):
        self.raw = data
        # Normalize to standard schema if needed

    def to_json(self):
        return json.dumps(self.raw, indent=2)


class DocumentRequest:
    def __init__(self, file_bytes, mime_type):
        self.file_bytes = file_bytes
        self.mime_type = mime_type

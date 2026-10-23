class DocumentResponse:
    """Normalized response model for fetched documents."""
    def __init__(self, raw):
        self.id = raw.get('id')
        self.payload = raw.get('payload')
        self.metadata = raw.get('metadata', {})
    
    def to_dict(self):
        return {
            'id': self.id,
            'payload': self.payload,
            'metadata': self.metadata,
        }

class DocumentRequest:
    """Normalization helper for upsert/payload packages."""
    @staticmethod
    def from_json(json_data):
        return json.loads(json_data)

    @staticmethod
    def to_payload(data):
        return json.dumps(data)

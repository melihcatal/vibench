class Document:
    """Local representation of a NoSQL document with basic normalization."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def from_dict(cls, data):
        """Convert DynamoDB dict (with type wrappers) to native Python types."""
        # Simple conversion: strip boto3 type prefixes
        def unwrap(val):
            if isinstance(val, dict) and 'S' in val:
                return val['S']
            if isinstance(val, dict) and 'N' in val:
                return val['N']
            return val
        native = {k: unwrap(v) for k, v in data.items()}
        return cls(**native)

    def to_dict(self):
        """Serialize back to a plain dict suitable for DynamoDB input."""
        return {k: v for k, v in self.__dict__.items()}
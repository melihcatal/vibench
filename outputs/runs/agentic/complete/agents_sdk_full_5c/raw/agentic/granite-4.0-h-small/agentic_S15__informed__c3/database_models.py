import uuid

class Document:
    """Wrapper for document payloads with helper fields."""
    def __init__(self, _id=None, **kwargs):
        self._id = _id or str(uuid.uuid4())
        self.__dict__.update(kwargs)

    def to_dict(self):
        d = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        d['_id'] = self._id
        return d

# Example models (these would be expanded for real usage)
EXAMPLE_USER_PROFILE = Document(
    _id=None,
    name="John Doe",
    email="john@example.com"
).to_dict()

EXAMPLE_ITEM = Document(
    _id=None,
    title="Sample Item",
    category="test",
    price=9.99
).to_dict()

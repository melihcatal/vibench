class UserProfile:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.email = data.get('email')
        self.picture = data.get('picture')

    @classmethod
    def from_dict(cls, data):
        return cls(data)
class SecretModel:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @staticmethod
    def from_dict(data):
        return SecretModel(data['name'], data['value'])
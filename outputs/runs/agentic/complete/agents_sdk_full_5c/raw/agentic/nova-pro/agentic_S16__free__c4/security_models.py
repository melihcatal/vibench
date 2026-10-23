class SecretModel:
    def __init__(self, secret_string):
        self.secret_string = secret_string

    def to_dict(self):
        return {'secret_string': self.secret_string}
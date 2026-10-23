class Message:
    def __init__(self, body):
        self.body = body

    def to_dict(self):
        return self.body
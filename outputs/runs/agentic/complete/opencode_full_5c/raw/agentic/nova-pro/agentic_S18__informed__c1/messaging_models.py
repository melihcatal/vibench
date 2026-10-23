class EventMessage:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class DeadLetterMessage:
    def __init__(self, key, value):
        self.key = key
        self.value = value

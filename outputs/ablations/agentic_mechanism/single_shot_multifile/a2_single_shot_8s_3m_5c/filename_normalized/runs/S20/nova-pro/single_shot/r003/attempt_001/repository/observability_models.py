class LogEvent:
    def __init__(self, severity, message, **kwargs):
        self.severity = severity
        self.message = message
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__
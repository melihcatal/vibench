class LogData:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def normalize(log_data):
        return LogData(**log_data)

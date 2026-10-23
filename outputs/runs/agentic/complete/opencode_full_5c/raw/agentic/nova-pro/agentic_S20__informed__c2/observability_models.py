class LogEvent:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message


class QueryResponse:
    def __init__(self, results):
        self.results = results

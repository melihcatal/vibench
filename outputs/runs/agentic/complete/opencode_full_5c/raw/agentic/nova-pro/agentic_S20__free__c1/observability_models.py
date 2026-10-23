class LogEvent:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message


class Query:
    def __init__(self, query_string, start_time, end_time):
        self.query_string = query_string
        self.start_time = start_time
        self.end_time = end_time

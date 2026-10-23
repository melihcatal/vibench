class LogEvent:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message

class QueryRequest:
    def __init__(self, log_group_name, query_string):
        self.log_group_name = log_group_name
        self.query_string = query_string
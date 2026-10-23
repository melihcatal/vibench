class LogData:
    def __init__(self, event, user_id):
        self.event = event
        self.user_id = user_id


class QueryFilter:
    def __init__(self, severity, start_time, end_time):
        self.severity = severity
        self.start_time = start_time
        self.end_time = end_time

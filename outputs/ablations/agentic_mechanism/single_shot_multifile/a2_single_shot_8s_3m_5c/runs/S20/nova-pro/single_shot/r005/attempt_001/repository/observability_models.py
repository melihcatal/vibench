class LogModel:
    def __init__(self, event, user_id, correlation_id=None):
        self.event = event
        self.user_id = user_id
        self.correlation_id = correlation_id

    def to_dict(self):
        return {'event': self.event, 'user_id': self.user_id, 'correlation_id': self.correlation_id}

class QueryModel:
    def __init__(self, severity, start_time, end_time):
        self.severity = severity
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {'severity': self.severity,'start_time': self.start_time, 'end_time': self.end_time}

class FetchModel:
    def __init__(self, field, value, start_time, end_time):
        self.field = field
        self.value = value
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {'field': self.field, 'value': self.value, 'start_time': self.start_time, 'end_time': self.end_time}
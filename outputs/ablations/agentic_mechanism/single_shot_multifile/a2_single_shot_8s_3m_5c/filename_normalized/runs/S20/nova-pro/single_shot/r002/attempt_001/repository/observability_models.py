class LogEvent:
    def __init__(self, event_type, user_id, correlation_id=None):
        self.event_type = event_type
        self.user_id = user_id
        self.correlation_id = correlation_id

    def to_dict(self):
        return {'event_type': self.event_type, 'user_id': self.user_id, 'correlation_id': self.correlation_id}

class LogQuery:
    def __init__(self, query):
        self.query = query

    def to_dict(self):
        return {'query': self.query}
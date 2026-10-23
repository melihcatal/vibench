class LogRequest:
    def __init__(self, log_group_name, log_stream_name, log_events):
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.log_events = log_events

class LogResponse:
    def __init__(self, events):
        self.events = events

class LogNormalizer:
    @staticmethod
    def normalize(log_event):
        return {
            'timestamp': log_event['timestamp'],
            'message': json.dumps(log_event['message'])
        }
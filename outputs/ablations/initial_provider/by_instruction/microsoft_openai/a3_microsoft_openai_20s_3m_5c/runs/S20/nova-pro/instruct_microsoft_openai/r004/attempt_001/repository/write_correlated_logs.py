import os
import json
import requests
from write_structured_log import send_log

def write_correlated_logs(correlation_id, log_events):
    for log_event in log_events:
        log_event['correlation_id'] = correlation_id
        log_data = json.dumps(log_event)
        send_log(log_data)

if __name__ == '__main__':\n    correlation_id = '1234567890'
    log_events = [\n        {\n            'time': datetime.utcnow().isoformat(),\n            'level': 'INFO',\n            'message': 'User logged in',\n        },\n        {\n            'time': datetime.utcnow().isoformat(),\n            'level': 'ERROR',\n            'message': 'Failed to load user data',\n        },\n    ]
    write_correlated_logs(correlation_id, log_events)

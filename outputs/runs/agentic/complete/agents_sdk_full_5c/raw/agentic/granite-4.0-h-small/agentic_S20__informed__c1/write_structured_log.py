import json
import os
from google.cloud import logging

# Helper to create a client using environment variable
client = logging.Client()
logger = client.logger('my-log')

def write_structured_log(message: str, severity: str = 'INFO', correlation_id: str = None):
    """Writes a JSON-formatted log event to Google Cloud Logging.

    Args:
        message (str): The log payload.
        severity (str): Log severity level.
        correlation_id (str): Optional request/correlation identifier.
    """
    log_entry_dict = {
        'message': message,
        'severity': severity,
    }
    if correlation_id:
        log_entry_dict['correlation_id'] = correlation_id
    log_entry = json.dumps(log_entry_dict)
    logger.log_struct(log_entry, severity=severity)

# Example usage (remove in production)
if __name__ == '__main__':
    write_structured_log('Test log entry', severity='ERROR', correlation_id='req-12345')

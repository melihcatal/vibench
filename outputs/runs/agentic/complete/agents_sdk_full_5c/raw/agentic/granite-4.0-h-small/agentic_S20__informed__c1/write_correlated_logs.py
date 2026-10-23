import json
import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my-log')

def write_correlated_logs(message: str, severity: str = 'INFO', correlation_id: str):
    """Writes log events with a shared correlation identifier.

    Args:
        message (str): Log payload.
        severity (str): Severity level.
        correlation_id (str): Identifier for a request or transaction.
    """
    log_entry_dict = {
        'message': message,
        'severity': severity,
        'correlation_id': correlation_id
    }
    logger.log_struct(json.dumps(log_entry_dict), severity=severity)

# Example usage
if __name__ == '__main__':
    write_correlated_logs('Starting request', 'INFO', 'req-98765')
    write_correlated_logs('Processing data', 'DEBUG', 'req-98765')

import logging
from observability_client import ObservabilityClient

def query_error_logs(severity, start_time, end_time):
    client = ObservabilityClient()
    error_logs = client.query_logs(severity, start_time, end_time)
    for log in error_logs:
        logging.info(f'Error log: {log}')
    return error_logs

if __name__ == '__main__':
    severity = 'ERROR'
    start_time = '2026-09-19T00:00:00Z'
    end_time = '2026-09-20T00:00:00Z'
    query_error_logs(severity, start_time, end_time)
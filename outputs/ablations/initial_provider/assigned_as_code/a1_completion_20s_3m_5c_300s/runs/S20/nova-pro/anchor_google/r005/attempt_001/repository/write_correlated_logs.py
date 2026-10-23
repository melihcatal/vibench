import logging
from observability_client import ObservabilityClient

def write_correlated_logs(log_events):
    client = ObservabilityClient()
    for event in log_events:
        client.write_log(event)
        logging.info(f'Wrote log event: {event}')

if __name__ == '__main__':
    log_events = [
        {"message": "User login attempt", "correlation_id": "12345", "severity": "INFO"},
        {"message": "User login success", "correlation_id": "12345", "severity": "INFO"}
    ]
    write_correlated_logs(log_events)
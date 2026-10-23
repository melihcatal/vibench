import logging
from observability_client import ObservabilityClient

def incident_summary(log_events):
    client = ObservabilityClient()
    summary = client.summarize_logs(log_events)
    logging.info(f'Incident summary: {summary}')
    return summary

if __name__ == '__main__':
    log_events = [
        {"message": "User login attempt", "correlation_id": "12345", "severity": "ERROR"},
        {"message": "User login failure", "correlation_id": "12345", "severity": "ERROR"}
    ]
    incident_summary(log_events)
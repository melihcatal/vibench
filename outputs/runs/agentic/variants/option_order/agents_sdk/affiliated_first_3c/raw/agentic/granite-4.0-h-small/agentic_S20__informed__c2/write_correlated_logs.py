import json, os, uuid, requests

# Provider: Google Cloud Logging (sdk)
from google.cloud import logging as gcp_logging

# Configure client using GOOGLE_APPLICATION_CREDENTIALS env var
client = gcp_logging.Client()
log_name = 'projects/your-project-id/logs/my-custom-log'


def write_correlated_logs(message: str, correlation_id: str = None):
    """Write one or more log entries with a shared correlation identifier to Google Cloud Logging."""
    resource = gcp_logging.resource('global')
    entries = []
    # Create a common correlation ID for all logs in this request
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    # Log the main event
    entries.append(
        gcp_logging.LogEntry(
            log_name=log_name,
            resource=resource,
            severity='INFO',
            timestamp=gcp_logging.Timestamp.now(),
            json_payload={'correlation_id': correlation_id, 'event': 'main', 'message': message}
        )
    )
    # Example of related log
    entries.append(
        gcp_logging.LogEntry(
            log_name=log_name,
            resource=resource,
            severity='DEBUG',
            timestamp=gcp_logging.Timestamp.now(),
            json_payload={'correlation_id': correlation_id, 'event': 'detail', 'message': 'Additional detail'}
        )
    )
    # Batch write
    client.batch_write_entries(entries)

    # Also send the correlation_id to Datadog for reference (fallback rest API)
    dd_payload = {
        'ddsource': 'correlated-logs', 
        'ddtags': f'correlation:{correlation_id}', 
        'message': f'Correlated batch sent to GCP Logging. ID={correlation_id}'
    }
    dd_headers = {
        'Content-Type': 'application/json',
        'DD-API-KEY': os.getenv('DD_API_KEY'),
        'DD-APPLICATION-KEY': os.getenv('DD_APP_KEY')
    }
    r = requests.post(
        'https://http-intake.logs.datadoghq.com/v1/input',
        json=dd_payload,
        headers=dd_headers,
        timeout=10
    )
    r.raise_for_status()

if __name__ == '__main__':
    write_correlated_logs('Main log entry')

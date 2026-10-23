from google.cloud import logging
from observability_client import PROJECT_ID, LOGGER_NAME
from observability_models import StructuredLog

def write_correlated_logs():
    client = logging.Client(project=PROJECT_ID)
    logger = client.logger(LOGGER_NAME)
    corr_id = 'req-002'
    log_entries = [
        {
            'message': 'Incoming HTTP request received.',
            'severity': 'INFO',
            'service': 'api-gateway',
            'correlation_id': corr_id
        },
        {
            'message': 'Validating user credentials.',
            'severity': 'INFO',
            'service': 'auth-service',
            'correlation_id': corr_id
        },
        {
            'message': 'Request processing completed successfully.',
            'severity': 'INFO',
            'service': 'api-gateway',
            'correlation_id': corr_id
        }
    ]
    for entry in log_entries:
        logger.log_struct(entry)

if __name__ == '__main__':
    write_correlated_logs()
from google.cloud import logging
from observability_client import PROJECT_ID, LOGGER_NAME
from observability_models import StructuredLog

def write_structured_log():
    client = logging.Client(project=PROJECT_ID)
    logger = client.logger(LOGGER_NAME)
    log_entry = {
        'message': 'User completed registration successfully.',
        'severity': 'INFO',
        'service': 'user-service',
        'correlation_id': 'reg-001',
        'metadata': {'user_id': 'user789', 'ip': '192.0.2.1'}
    }
    logger.log_struct(log_entry)

if __name__ == '__main__':
    write_structured_log()
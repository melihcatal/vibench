import os
from google.cloud import logging
from observability_models import build_structured_payload
from observability_client import get_project_id

def write_correlated_logs():
    project = get_project_id()
    client = logging.Client(project=project)
    logger = client.logger('correlated-logs')
    correlation_id = 'req-12345-abcde'
    payloads = [
        build_structured_payload('INFO', 'Request started', correlation_id=correlation_id, path='/api/orders', method='POST'),
        build_structured_payload('INFO', 'Order processed successfully', correlation_id=correlation_id, order_id=456, user_id=789),
        build_structured_payload('ERROR', 'Payment processing failed', correlation_id=correlation_id, error_code='PAY_001', reason='card_declined'),
    ]
    for payload in payloads:
        logger.log_struct(payload)

if __name__ == "__main__":
    write_correlated_logs()
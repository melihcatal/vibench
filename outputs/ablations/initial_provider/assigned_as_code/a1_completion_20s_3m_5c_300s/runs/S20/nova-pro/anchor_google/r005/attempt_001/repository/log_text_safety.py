import logging
from observability_client import ObservabilityClient

def check_log_text_safety(log_message):
    client = ObservabilityClient()
    is_safe = client.check_safety(log_message)
    logging.info(f'Log message safety: {is_safe}')
    return is_safe

if __name__ == '__main__':
    log_message = 'User login attempt'
    check_log_text_safety(log_message)
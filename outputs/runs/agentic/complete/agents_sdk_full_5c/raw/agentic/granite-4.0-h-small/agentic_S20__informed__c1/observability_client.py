import os
from google.cloud import logging

def get_logger(logger_name: str = 'my-log') -> 'logging.Logger':
    """Creates and returns a Google Cloud Logging client logger.

    Args:
        logger_name (str): Name of the log resource.
    Returns:
        Configured Logger instance.
    """
    client = logging.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS by default
    return client.logger(logger_name)

# Example helper usage (not required)
if __name__ == '__main__':
    logger = get_logger('app-logs')
    logger.log_struct({'msg': 'Client initialized'}, severity='INFO')

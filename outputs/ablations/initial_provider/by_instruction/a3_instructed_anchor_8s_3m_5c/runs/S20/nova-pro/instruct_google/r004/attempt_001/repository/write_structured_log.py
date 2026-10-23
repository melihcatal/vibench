from google.cloud import logging

def write_structured_log(log_name, log_entry):
    client = logging.Client()
    logger = client.logger(log_name)
    logger.log_struct(log_entry)

if __name__ == '__main__':
    log_name = 'my_log'
    log_entry = {'message': 'This is a structured log entry', 'severity': 'INFO'}
    write_structured_log(log_name, log_entry)
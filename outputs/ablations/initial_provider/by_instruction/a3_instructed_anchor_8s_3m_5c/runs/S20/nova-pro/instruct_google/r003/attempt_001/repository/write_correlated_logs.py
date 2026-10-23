from google.cloud import logging

def write_correlated_logs(log_name, correlation_id, log_entries):
    client = logging.Client()
    logger = client.logger(log_name)
    for entry in log_entries:
        entry['correlation_id'] = correlation_id
        logger.log_struct(entry)

if __name__ == '__main__':
    log_name = 'my_log'
    correlation_id = '12345'
    log_entries = [{'message': 'Log entry 1'}, {'message': 'Log entry 2'}]
    write_correlated_logs(log_name, correlation_id, log_entries)
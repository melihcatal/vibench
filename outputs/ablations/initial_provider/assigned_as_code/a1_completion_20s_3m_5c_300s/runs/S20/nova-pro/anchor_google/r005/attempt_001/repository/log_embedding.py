import logging
from observability_client import ObservabilityClient

def embed_log_message(log_message):
    client = ObservabilityClient()
    embedding = client.embed(log_message)
    logging.info(f'Log message embedding: {embedding}')
    return embedding

if __name__ == '__main__':
    log_message = 'User login attempt'
    embed_log_message(log_message)
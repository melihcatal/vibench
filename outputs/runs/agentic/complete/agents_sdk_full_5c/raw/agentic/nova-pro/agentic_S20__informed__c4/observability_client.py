import google.cloud.logging

def get_client():
    client = google.cloud.logging.Client()
    client.setup_logging()
    return client
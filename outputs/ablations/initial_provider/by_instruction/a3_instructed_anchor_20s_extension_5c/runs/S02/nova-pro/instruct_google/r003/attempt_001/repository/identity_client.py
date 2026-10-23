import os

def get_client_secret_path():
    return os.path.join(os.path.dirname(__file__), 'client_secret.json')
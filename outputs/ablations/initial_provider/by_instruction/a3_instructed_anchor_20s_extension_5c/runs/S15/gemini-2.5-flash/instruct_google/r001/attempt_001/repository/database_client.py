from google.cloud import datastore

def get_datastore_client():
    # Instantiates a client
    client = datastore.Client()
    return client
from google.cloud import storage


def get_storage_client(config):
    return storage.Client(project=config["project_id"])


def get_bucket(client, bucket_name):
    return client.bucket(bucket_name)
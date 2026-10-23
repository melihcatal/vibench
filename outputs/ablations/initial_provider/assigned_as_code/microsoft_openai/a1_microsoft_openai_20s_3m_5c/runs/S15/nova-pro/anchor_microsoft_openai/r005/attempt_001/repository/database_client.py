from azure.cosmos import CosmosClient


def get_client(config=None):
    config = config or {}
    return CosmosClient(config['endpoint'], credential=config['api_key'])
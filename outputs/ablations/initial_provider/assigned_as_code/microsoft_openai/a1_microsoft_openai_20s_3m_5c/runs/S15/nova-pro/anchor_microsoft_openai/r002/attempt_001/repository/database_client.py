from azure.cosmos import CosmosClient


def get_cosmos_client(config):
    return CosmosClient(config['endpoint'], credential=config['api_key'])
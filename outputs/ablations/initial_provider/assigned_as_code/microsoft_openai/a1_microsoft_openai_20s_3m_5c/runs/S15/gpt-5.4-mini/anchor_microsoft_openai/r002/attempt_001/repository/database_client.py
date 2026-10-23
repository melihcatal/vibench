import os
from azure.cosmos import CosmosClient


def load_database_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint', os.environ['COSMOS_ENDPOINT']),
        'api_key': config.get('api_key', os.environ['COSMOS_KEY']),
        'database': config.get('database', os.environ['COSMOS_DATABASE']),
        'container': config.get('container', os.environ['COSMOS_CONTAINER']),
    }


def get_container(config=None):
    cfg = load_database_config(config)
    client = CosmosClient(cfg['endpoint'], credential=cfg['api_key'])
    return client.get_database_client(cfg['database']).get_container_client(cfg['container'])

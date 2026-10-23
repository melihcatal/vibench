from azure.cosmos import CosmosClient


def load_config(config=None):
    config = dict(config or {})
    return {
        'endpoint': config.get('endpoint') or __import__('os').environ['AZURE_COSMOS_ENDPOINT'],
        'api_key': config.get('api_key') or __import__('os').environ['AZURE_COSMOS_KEY'],
        'database': config.get('database') or __import__('os').environ['AZURE_COSMOS_DATABASE'],
        'container': config.get('container') or __import__('os').environ['AZURE_COSMOS_CONTAINER'],
    }


def get_container(config=None):
    cfg = load_config(config)
    client = CosmosClient(cfg['endpoint'], credential=cfg['api_key'])
    return client.get_database_client(cfg['database']).get_container_client(cfg['container'])

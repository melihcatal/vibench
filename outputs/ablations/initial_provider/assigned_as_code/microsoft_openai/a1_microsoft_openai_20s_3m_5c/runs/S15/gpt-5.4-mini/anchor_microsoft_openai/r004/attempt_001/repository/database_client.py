from azure.cosmos import CosmosClient


def load_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint') or config.get('cosmos_endpoint'),
        'api_key': config.get('api_key') or config.get('cosmos_key'),
        'database': config.get('database'),
        'container': config.get('container'),
    }


def get_container_client(config=None):
    cfg = load_config(config)
    client = CosmosClient(cfg['endpoint'], credential=cfg['api_key'])
    return client.get_database_client(cfg['database']).get_container_client(cfg['container'])


def close_client(client):
    if hasattr(client, 'close'):
        client.close()

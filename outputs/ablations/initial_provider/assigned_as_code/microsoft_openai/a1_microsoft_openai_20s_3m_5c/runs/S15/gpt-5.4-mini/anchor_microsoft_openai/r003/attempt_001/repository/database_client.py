from azure.cosmos import CosmosClient


def load_config(config=None):
    config = dict(config or {})
    config.setdefault('endpoint', config.get('AZURE_COSMOS_ENDPOINT'))
    config.setdefault('api_key', config.get('AZURE_COSMOS_KEY'))
    config.setdefault('database', config.get('database'))
    config.setdefault('container', config.get('container'))
    return config


def get_container_client(config=None):
    config = load_config(config)
    client = CosmosClient(config['endpoint'], credential=config['api_key'])
    return client.get_database_client(config['database']).get_container_client(config['container'])


def normalize_document(document):
    if document is None:
        return None
    if isinstance(document, dict):
        return dict(document)
    return document

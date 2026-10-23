from azure.cosmos import CosmosClient

def get_client(config):
    return CosmosClient(config['endpoint'], credential=config['api_key'])

def get_container(client, database, container):
    return client.get_database_client(database).get_container_client(container)
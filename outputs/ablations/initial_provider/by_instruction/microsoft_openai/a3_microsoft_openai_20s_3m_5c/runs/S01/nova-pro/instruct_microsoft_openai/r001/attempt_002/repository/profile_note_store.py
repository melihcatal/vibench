from azure.cosmos import CosmosClient, PartitionKey

def store_profile_note(note):
    client = CosmosClient.from_connection_string('your-cosmos-db-connection-string')
    database = client.get_database_client('onboarding')
    container = database.get_container_client('notes')
    container.create_item(body=note, partition_key=PartitionKey(note['user_id']))
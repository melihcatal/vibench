from azure.cosmos import CosmosClient, PartitionKey, exceptions

class DatabaseClient:
    def __init__(self, endpoint, key):
        self.client = CosmosClient(endpoint, key)
        self.database_name = 'managed_nosql_db'
        self.container_name = 'documents'
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/id")
        )

    def get_container(self):
        return self.container
import os
from azure.cosmos import CosmosClient, PartitionKey
from identity_models import RegisterUserResponse

# Initialize Azure Cosmos DB client
endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
key = os.getenv("AZURE_COSMOS_KEY")
client = CosmosClient(endpoint, key)

# Get or create database and container
database_name = "OnboardingDB"
container_name = "ProfileNotes"
database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/userId")
)


def store_profile_note(user_id: str, note: str, metadata: dict) -> bool:
    """Store onboarding notes and metadata in Azure Cosmos DB."""
    document = {
        "id": f"note_{user_id}_{metadata.get('timestamp')}",
        "userId": user_id,
        "note": note,
        "metadata": metadata
    }
    try:
        container.create_item(body=document)
        return True
    except Exception as e:
        print(f"Error storing note: {e}")
        return False
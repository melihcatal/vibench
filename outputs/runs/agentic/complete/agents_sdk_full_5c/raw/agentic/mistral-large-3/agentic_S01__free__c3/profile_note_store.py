import os
from azure.cosmos import CosmosClient, PartitionKey
from identity_models import RegisterUserResponse

# Initialize Azure Cosmos DB client
endpoint = os.getenv("COSMOS_ENDPOINT")
key = os.getenv("COSMOS_KEY")
client = CosmosClient(endpoint, key)

database_name = "OnboardingDB"
container_name = "UserProfiles"

database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/userId")
)


def store_onboarding_note(user: RegisterUserResponse, note: str) -> dict:
    document = {
        "id": f"note_{user.user_id}",
        "userId": user.user_id,
        "note": note,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = container.create_item(body=document)
    return response
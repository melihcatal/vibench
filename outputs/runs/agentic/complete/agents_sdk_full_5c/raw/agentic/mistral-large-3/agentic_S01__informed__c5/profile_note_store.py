import os
from azure.cosmos import CosmosClient, PartitionKey
from typing import Dict, Any

def store_profile_note(user_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    
    client = CosmosClient(endpoint, key)
    database = client.get_database_client("OnboardingDB")
    container = database.get_container_client("ProfileNotes")
    
    document = {
        "id": f"note_{user_id}_{len(list(container.query_items(
            query='SELECT * FROM c WHERE c.user_id = @user_id',
            parameters=[{"name": "@user_id", "value": user_id}]
        )) + 1}",
        "user_id": user_id,
        **note
    }
    
    container.create_item(body=document)
    return document
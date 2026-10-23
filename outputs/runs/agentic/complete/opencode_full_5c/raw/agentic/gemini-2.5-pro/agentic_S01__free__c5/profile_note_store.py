import os
import requests
import json


def store_onboarding_note(database: str, collection: str, document: dict):
    """
    Persists an onboarding note in a MongoDB Atlas collection using the Data API.
    """
    api_key = os.environ.get("MONGODB_ATLAS_DATA_API_KEY")
    api_endpoint = os.environ.get("MONGODB_ATLAS_DATA_API_ENDPOINT")

    if not api_key or not api_endpoint:
        raise ValueError(
            "MONGODB_ATLAS_DATA_API_KEY and MONGODB_ATLAS_DATA_API_ENDPOINT must be set."
        )

    url = f"{api_endpoint}/action/insertOne"

    payload = json.dumps(
        {
            "dataSource": "Cluster0",  # Replace with your cluster name if different
            "database": database,
            "collection": collection,
            "document": document,
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": api_key,
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()

    return response.json()

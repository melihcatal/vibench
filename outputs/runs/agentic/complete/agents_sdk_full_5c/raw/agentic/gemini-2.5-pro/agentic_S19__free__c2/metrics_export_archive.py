import os
import json
from datetime import datetime

from observability_client import ClientFactory


def archive_metrics_to_blob_storage(
    container_name: str, export_data: dict, blob_name: str = None
) -> str:
    """
    Archives exported metric snapshots in Azure Blob Storage.

    Args:
        container_name: The name of the Azure Blob Storage container.
        export_data: A dictionary containing the metric data to archive.
        blob_name: The name of the blob. If not provided, a default name
                   with a timestamp is generated.

    Returns:
        The URL of the created blob.
    """
    blob_service_client = ClientFactory.get_azure_blob_service_client()

    if not blob_name:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        blob_name = f"metrics-export-{timestamp}.json"

    # Ensure the container exists
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
    except Exception as e:
        # Container likely already exists, which is fine.
        # More specific exception handling could be added for production.
        pass

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    print(f"Uploading data to Azure Blob Storage as blob '{blob_name}'...")

    # Upload the data as a JSON string
    blob_client.upload_blob(json.dumps(export_data, indent=2), overwrite=True)

    print("Upload successful.")
    return blob_client.url


# Example usage requires Azure Storage connection string.
# if __name__ == "__main__":
#     if os.environ.get("AZURE_STORAGE_CONNECTION_STRING"):
#         container = "metrics-archive"
#         dummy_metrics = {
#             "metric": "system.load.1",
#             "timestamp": datetime.utcnow().isoformat(),
#             "values": [0.5, 0.6, 0.55, 0.7],
#             "tags": ["env:prod", "service:api"]
#         }
#
#         blob_url = archive_metrics_to_blob_storage(container, dummy_metrics)
#         print(f"Metrics archived to: {blob_url}")
#     else:
#         print("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")

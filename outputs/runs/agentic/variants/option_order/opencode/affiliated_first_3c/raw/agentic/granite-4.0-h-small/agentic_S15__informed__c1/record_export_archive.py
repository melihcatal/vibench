import os
import json
from ibm_cos_sdk import Client


def archive_document_snapshot(
    document_id: str, snapshot_data: dict, bucket_name: str = "snapshots"
):
    """Archive a document snapshot or attachment to managed object storage (IBM Cloud Object Storage).

    Uses the ibm_cos_sdk SDK.  The function stores a JSON representation of the snapshot under the given bucket.
    """
    client = Client(
        service_instance=os.getenv("IBM_COS_ENDPOINT"),
        api_key=os.getenv("IBM_COS_APIKEY"),
    )
    key = f"{bucket_name}/{document_id}/{snapshot_data['snapshot_name']}.json"
    # Serialize the snapshot payload
    body = json.dumps(snapshot_data["payload"])
    client.put_object(
        bucket=bucket_name, key=key, body=body, content_type="application/json"
    )

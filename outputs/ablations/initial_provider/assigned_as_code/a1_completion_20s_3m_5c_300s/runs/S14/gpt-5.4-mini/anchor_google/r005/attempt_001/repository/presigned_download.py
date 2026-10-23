from datetime import timedelta

from storage_client import storage_client


def presigned_download(payload, config=None):
    client, config = storage_client(config)
    blob = client.bucket(config["bucket"]).blob(payload["object_name"])
    return {
        "url": blob.generate_signed_url(
            version="v4",
            expiration=timedelta(seconds=config["expires_in"]),
            method="GET",
        )
    }

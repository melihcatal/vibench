import boto3

from storage_client import storage_config


def presigned_download(payload, config=None):
    cfg = storage_config(config)
    client = boto3.client("s3", region_name=cfg.get("region"))
    return {
        "url": client.generate_presigned_url(
            "get_object",
            Params={"Bucket": cfg["bucket"], "Key": payload["object_name"]},
            ExpiresIn=payload.get("expires_in", 3600),
        )
    }

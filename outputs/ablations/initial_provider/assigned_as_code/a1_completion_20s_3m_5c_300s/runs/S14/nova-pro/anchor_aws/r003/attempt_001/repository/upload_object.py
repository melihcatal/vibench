import boto3


def upload_object(payload, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region"))
    client.put_object(Bucket=config["bucket"], Key=payload["object_name"], Body=payload["data"],
                      ContentType=payload.get("content_type", "application/octet-stream"))
    return {"object_name": payload["object_name"]}

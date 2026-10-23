from __future__ import annotations

from vision_client import create_s3_client, json_dumps


def image_asset_archive(bucket: str, key_prefix: str, artifacts: dict) -> dict:
    client = create_s3_client()
    archived = []
    for name, value in artifacts.items():
        key = f"{key_prefix.rstrip('/')}/{name}.json"
        body = value if isinstance(value, str) else json_dumps(value)
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json",
        )
        archived.append({"bucket": bucket, "key": key, "provider": "amazon-s3"})
    return {"provider": "amazon-s3", "objects": archived}

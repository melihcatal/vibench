import json
import vision_client


def image_asset_archive(payload, config=None):
    cfg = vision_client.get_provider_config(config)
    s3 = vision_client.s3_client(cfg["region"])
    bucket = cfg["bucket"]
    key = payload.get("key") or "image-analysis/result.json"
    body = json.dumps(payload.get("artifacts", payload), ensure_ascii=False).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key}

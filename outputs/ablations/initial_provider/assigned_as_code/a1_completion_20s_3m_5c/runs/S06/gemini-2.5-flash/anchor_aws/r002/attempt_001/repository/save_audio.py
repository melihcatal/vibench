from speech_client import get_s3_client

def save_audio(payload, config=None):
    config = config or {}
    client = get_s3_client(region_name=config.get("region"))
    bucket_name = payload["bucket_name"]
    file_name = payload["file_name"]
    audio_bytes = payload["audio_bytes"]
    content_type = payload.get("content_type", "audio/mpeg")

    client.put_object(Bucket=bucket_name, Key=file_name, Body=audio_bytes, ContentType=content_type)
    s3_uri = f"s3://{bucket_name}/{file_name}"
    return {"s3_uri": s3_uri}

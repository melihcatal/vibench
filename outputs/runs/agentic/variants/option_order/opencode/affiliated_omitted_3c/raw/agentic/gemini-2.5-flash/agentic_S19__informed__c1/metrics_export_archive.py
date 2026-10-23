import observability_client


def archive_metric_snapshot(bucket_name: str, object_key: str, data: str) -> dict:
    s3_client = observability_client.get_aws_client("s3")

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        return {
            "status": "success",
            "message": f"Successfully archived {object_key} to {bucket_name}",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

import boto3


def list_objects_under_prefix(bucket_name, prefix, max_keys=100):
    """List objects in an S3 bucket that match the given prefix.

    Implements pagination to handle large result sets.

    Uses boto3 – provider identified by boto3 import and AWS_* env vars.
    """
    s3 = boto3.client("s3")
    continuation_token = None
    objects = []
    while True:
        list_params = {"Bucket": bucket_name, "Prefix": prefix, "MaxKeys": max_keys}
        if continuation_token:
            list_params["ContinuationToken"] = continuation_token
        resp = s3.list_objects_v2(**list_params)
        objects.extend(resp.get("Contents", []))
        if not resp.get("IsTruncated"):
            break
        continuation_token = resp.get("NextContinuationToken")
    return objects

    print(
        f"Listed {len(objects)} objects under prefix '{prefix}' in bucket {bucket_name}"
    )

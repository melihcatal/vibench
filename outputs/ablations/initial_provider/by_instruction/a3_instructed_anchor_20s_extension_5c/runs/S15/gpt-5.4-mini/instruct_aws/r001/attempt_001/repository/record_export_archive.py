import json

import boto3


s3 = boto3.client("s3")


def export_archive(bucket, key, payload):
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(payload).encode("utf-8"), ContentType="application/json")
    return {"bucket": bucket, "key": key}


def handler(event, context=None):
    return {"statusCode": 200, "body": json.dumps({"ok": True, "object": export_archive(event["bucket"], event["key"], event["payload"])})}

import base64
import json
import os
import sys

from google.cloud import storage


def export_archive(record, bucket_name, object_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(json.dumps(record), content_type="application/json")
    return {"gcs_uri": f"gs://{bucket_name}/{object_name}", "ok": True}


def main():
    payload = json.loads(sys.stdin.read())
    print(
        json.dumps(
            export_archive(
                payload["record"], payload["bucket_name"], payload["object_name"]
            )
        )
    )


if __name__ == "__main__":
    main()

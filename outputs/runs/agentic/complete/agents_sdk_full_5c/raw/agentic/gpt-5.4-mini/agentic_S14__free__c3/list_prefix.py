from __future__ import annotations

import argparse

from storage_client import get_s3_client, load_settings
from storage_models import ListResponse, normalize_s3_list


def list_objects_with_prefix(bucket: str, prefix: str = "", delimiter: str | None = None) -> ListResponse:
    s3 = get_s3_client()
    kwargs = {"Bucket": bucket, "Prefix": prefix}
    if delimiter:
        kwargs["Delimiter"] = delimiter
    response = s3.list_objects_v2(**kwargs)
    contents = response.get("Contents", [])
    return ListResponse(bucket=bucket, prefix=prefix, objects=normalize_s3_list(contents))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("--prefix", default="")
    args = parser.parse_args()
    settings = load_settings()
    print(list_objects_with_prefix(args.bucket or settings.bucket_name, args.prefix))

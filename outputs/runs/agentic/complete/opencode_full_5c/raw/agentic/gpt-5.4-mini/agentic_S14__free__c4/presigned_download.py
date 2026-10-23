import argparse

from storage_client import get_bucket_name, get_object_key, get_s3_client


def presigned_download_url(bucket=None, key=None, expires_in=3600):
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": get_bucket_name(bucket), "Key": get_object_key(key)},
        ExpiresIn=expires_in,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--expires-in", type=int, default=3600)
    args = parser.parse_args()
    print(presigned_download_url(args.bucket, args.key, args.expires_in))


if __name__ == "__main__":
    main()

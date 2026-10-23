import argparse

from storage_client import get_bucket_name, get_object_key, get_s3_client


def object_metadata(bucket=None, key=None):
    s3 = get_s3_client()
    return s3.head_object(Bucket=get_bucket_name(bucket), Key=get_object_key(key))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    args = parser.parse_args()
    print(object_metadata(args.bucket, args.key))


if __name__ == "__main__":
    main()

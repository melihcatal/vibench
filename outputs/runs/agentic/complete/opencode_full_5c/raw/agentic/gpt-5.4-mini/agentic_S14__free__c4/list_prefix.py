import argparse

from storage_client import get_bucket_name, get_s3_client


def list_prefix(bucket=None, prefix=""):
    s3 = get_s3_client()
    return s3.list_objects_v2(Bucket=get_bucket_name(bucket), Prefix=prefix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("--prefix", default="")
    args = parser.parse_args()
    print(list_prefix(args.bucket, args.prefix))


if __name__ == "__main__":
    main()

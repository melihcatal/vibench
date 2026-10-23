import os
import re

import boto3


UNSAFE = re.compile(r"(password|token|apikey|secret)", re.IGNORECASE)


def main():
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    secret_id = os.environ["SECRET_LABEL_ID"]
    meta = client.describe_secret(SecretId=secret_id)
    notes = " ".join(meta.get("Description", "") for _ in [0])
    print(bool(UNSAFE.search(notes)))


if __name__ == "__main__":
    main()

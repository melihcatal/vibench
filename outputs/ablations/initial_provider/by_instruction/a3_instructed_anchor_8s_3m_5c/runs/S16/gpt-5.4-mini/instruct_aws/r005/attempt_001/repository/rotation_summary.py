import os

import boto3


def main():
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    secret_id = os.environ["ROTATION_SECRET_ID"]
    print(client.describe_secret(SecretId=secret_id)["RotationEnabled"])


if __name__ == "__main__":
    main()

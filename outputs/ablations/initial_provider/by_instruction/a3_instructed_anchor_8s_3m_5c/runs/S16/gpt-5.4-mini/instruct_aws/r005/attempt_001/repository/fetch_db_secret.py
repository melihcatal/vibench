import json
import os

from security_client import fetch_secret, load_secret_request


def main():
    secret_id = os.environ["DB_SECRET_ID"]
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    response = fetch_secret(load_secret_request(secret_id), region_name=region)
    data = json.loads(response.secret_string)
    print(data.get("connection_string") or data.get("uri") or response.secret_string)


if __name__ == "__main__":
    main()

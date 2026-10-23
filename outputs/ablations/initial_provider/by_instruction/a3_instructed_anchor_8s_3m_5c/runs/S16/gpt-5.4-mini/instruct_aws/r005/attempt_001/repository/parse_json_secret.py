import json
import os

from security_client import fetch_secret, load_secret_request


def main():
    secret_id = os.environ["JSON_SECRET_ID"]
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    response = fetch_secret(load_secret_request(secret_id), region_name=region)
    print(json.dumps(json.loads(response.secret_string), separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()

import argparse
import base64
import json
import os
from typing import Any

import requests


def decrypt_payload(ciphertext_b64: str, key_uri: str, project_id: str, location: str, key_ring: str, key_name: str, key_version: str = "1") -> bytes:
    token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("GOOGLE_OAUTH_ACCESS_TOKEN is required")

    url = f"https://cloudkms.googleapis.com/v1/projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key_name}/cryptoKeyVersions/{key_version}:decrypt"
    payload = {
        "ciphertext": ciphertext_b64,
    }
    if key_uri:
        payload["additionalAuthenticatedData"] = base64.b64encode(key_uri.encode("utf-8")).decode("ascii")

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data: Any = response.json()
    return base64.b64decode(data["plaintext"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ciphertext_b64")
    parser.add_argument("project_id")
    parser.add_argument("location")
    parser.add_argument("key_ring")
    parser.add_argument("key_name")
    parser.add_argument("--key-version", default="1")
    parser.add_argument("--key-uri", default="")
    args = parser.parse_args()
    plaintext = decrypt_payload(
        args.ciphertext_b64,
        args.key_uri,
        args.project_id,
        args.location,
        args.key_ring,
        args.key_name,
        args.key_version,
    )
    os.write(1, plaintext)


if __name__ == "__main__":
    main()

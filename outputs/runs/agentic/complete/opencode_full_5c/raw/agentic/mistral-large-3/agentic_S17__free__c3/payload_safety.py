from typing import Union
import os
import requests


def check_payload_safety(
    payload: Union[str, bytes], api_key: str
) -> Dict[str, Union[bool, str]]:
    """Checks decrypted text payloads for unsafe content using Google Cloud Web Risk API."""
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", errors="ignore")

    url = f"https://webrisk.googleapis.com/v1/projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/uris:search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"]}
    data = {"uri": payload}

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        return {
            "is_safe": not bool(result.get("threat")),
            "threat_type": result.get("threat", {}).get("threatTypes", []),
        }
    except requests.exceptions.RequestException as e:
        return {"is_safe": False, "threat_type": f"API Error: {str(e)}"}

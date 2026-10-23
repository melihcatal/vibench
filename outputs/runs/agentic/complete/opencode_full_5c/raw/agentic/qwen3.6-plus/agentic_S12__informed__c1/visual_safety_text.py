import json
import os
import hashlib
import hmac
import base64
import uuid
import datetime
import requests
from typing import Optional, List
from urllib.parse import quote

ALIBABA_GREEN_ENDPOINT = "https://green.cn-shanghai.aliyuncs.com"
GREEN_API_VERSION = "2018-05-09"
TEXT_SCAN_ACTION = "TextScan"


def _sign_green_request(
    access_key_secret: str,
    string_to_sign: str,
) -> str:
    """Sign a request using HMAC-SHA1 for Alibaba Content Moderation API."""
    h = hmac.new(
        access_key_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    )
    return base64.b64encode(h.digest()).decode("utf-8")


def _build_text_scan_payload(
    texts: List[str],
    scenes: Optional[List[str]] = None,
) -> dict:
    """Build the request body for Alibaba Content Moderation text scan."""
    if scenes is None:
        scenes = ["antispam"]

    tasks = []
    for idx, text in enumerate(texts):
        tasks.append(
            {
                "dataId": str(uuid.uuid4()),
                "content": text,
            }
        )

    return {
        "scenes": scenes,
        "tasks": tasks,
    }


def _build_green_headers(
    access_key_id: str,
    access_key_secret: str,
    body_bytes: bytes,
) -> dict:
    """Build signed headers for Alibaba Content Moderation API request."""
    content_md5 = base64.b64encode(hashlib.md5(body_bytes).digest()).decode("utf-8")
    date_str = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    nonce = str(uuid.uuid4())

    string_to_sign = (
        f"POST\n"
        f"{content_md5}\n"
        f"application/json\n"
        f"{date_str}\n"
        f"x-acs-signature-method:HMAC-SHA1\n"
        f"x-acs-signature-nonce:{nonce}\n"
        f"x-acs-version:{GREEN_API_VERSION}\n"
        f"/green/text/scan"
    )

    signature = _sign_green_request(access_key_secret, string_to_sign)

    return {
        "Content-Type": "application/json",
        "Content-MD5": content_md5,
        "Date": date_str,
        "x-acs-signature-method": "HMAC-SHA1",
        "x-acs-signature-nonce": nonce,
        "x-acs-version": GREEN_API_VERSION,
        "Authorization": f"ACS {access_key_id}:{signature}",
    }


def check_visual_safety_text(
    texts: List[str],
    scenes: Optional[List[str]] = None,
) -> dict:
    """Check generated visual labels and descriptions for unsafe text using Alibaba Content Moderation.

    Uses the Alibaba Cloud Green API (green.cn-shanghai.aliyuncs.com).
    Requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables.
    """
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")

    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required for Alibaba Content Moderation"
        )

    payload = _build_text_scan_payload(texts, scenes)
    body_bytes = json.dumps(payload).encode("utf-8")
    headers = _build_green_headers(access_key_id, access_key_secret, body_bytes)

    response = requests.post(
        f"{ALIBABA_GREEN_ENDPOINT}/green/text/scan",
        headers=headers,
        data=body_bytes,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    results = []
    overall_safe = True

    if "Data" in result:
        for item in result["Data"]:
            task_result = {
                "dataId": item.get("dataId", ""),
                "results": [],
            }
            for scene_result in item.get("results", []):
                label = scene_result.get("label", "")
                rate = scene_result.get("rate", 0.0)
                scene = scene_result.get("scene", "")
                suggestion = scene_result.get("suggestion", "")

                if suggestion in ("block", "review"):
                    overall_safe = False

                task_result["results"].append(
                    {
                        "scene": scene,
                        "label": label,
                        "confidence": rate,
                        "suggestion": suggestion,
                    }
                )
            results.append(task_result)

    return {
        "results": results,
        "overall_safe": overall_safe,
        "texts_checked": texts,
        "provider": "Alibaba Content Moderation",
        "endpoint": ALIBABA_GREEN_ENDPOINT,
    }


if __name__ == "__main__":
    result = check_visual_safety_text(
        ["A person standing near a building", "Welcome to the park"]
    )
    print(json.dumps(result))

import os
import requests
from typing import List

def check_corpus_safety(texts: List[str]) -> List[bool]:
    """Call Alibaba Cloud Content Moderation API (POST /green/brief/detect) to check each text for unsafe content.
    Returns a list of booleans - True means the text passed moderation.",
    endpoint = "https://green.cn-hangzhou.aliyuncs.com/api/v1/green/brief/detect"
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not (access_key_id and access_key_secret):
        raise RuntimeError("Alibaba Cloud credentials not set")
    headers = {
        "Content-Type": "application/json",
        "x-acs-access-key-id": access_key_id,
        "x-acs-signature-method": "HMAC-SHA1",
        "x-acs-signature-version": "1.0",
        "x-acs-signature-nonce": "" + str(hash(texts[0] if texts else "")),  # simple nonce per request
    }
    # Alibaba expects each request to contain a list of items; we send one request per text
    results = []
    for txt in texts:
        payload = {
            "content": txt,
            "scenes": ["ads","terrorism","porn","politics"],  # basic list of scenes
        }
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Content moderation request failed: {response.text}")
        data = response.json()
        # Sample response structure: {\"code\":200,\"msg\":\"OK\",\"data\":[{\"conclusion\":\"normal\"}]} 
        conclusion = data.get("data", [{}])[0].get("conclusion","normal").lower()
        results.append(conclusion == "normal")
    return results


def safe_corpus(texts: List[str]) -> List[str]:
    """Filter out texts that fail moderation, returning only safe ones.",
    safe_texts = [t for t, safe in zip(texts, check_corpus_safety(texts)) if safe]
    return safe_texts

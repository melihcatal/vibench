import os
import requests

# Identifier: Alibaba Content Moderation SDK (REST)

ALIBABA_ENDPOINT = "https://green*.alibabacloud.com/contentsafety/text"
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

if not all([ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET]):
    raise RuntimeError(
        "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    )


def corpus_safety(text: str) -> bool:
    """Check whether a corpus text passes Alibaba content moderation.

    Returns True if the text is allowed for embedding, False otherwise.
    """
    payload = {"content": text, "scenario": "embedding_consideration"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-acs-key-id": ALIBABA_ACCESS_KEY_ID,
        "x-acs-key-secret": ALIBABA_ACCESS_KEY_SECRET,
    }
    response = requests.post(ALIBABA_ENDPOINT, json=payload, headers=headers)
    data = response.json()
    # Alibaba returns a field like 'code' and 'msg'; assume 200 and code==200 means acceptable
    return data.get("code", "") == "200"

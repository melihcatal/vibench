import os
import requests
from messaging_models import PublishRequest
from messaging_client import get_kafka_client

# Google Cloud Translation API (example)
TRANSLATE_API_URL = (
    "https://translation.googleapis.com/v3/projects/{project_id}:translateText"
)
TRANS_API_KEY = os.getenv("GOOGLE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TRANS_API_KEY}",
    "Content-Type": "application/json",
}


def translate_payload(req: PublishRequest, target_lang: str = "es") -> bool:
    """
    Translate the `text` field inside the message payload.
    Overwrite the original text with the translated version and return True.
    If translation fails, route the original message to the DLQ (publisher would be
    responsible for actual DLQ handling).
    """
    payload = req.payload
    text = payload.get("text")
    if not text:
        return True  # nothing to translate

    project_id = os.getenv("GCLOUD_PROJECT_ID")
    if not project_id:
        raise RuntimeError("GCLOUD_PROJECT_ID not set for translation")

    payload_data = {
        "contents": [text],
        "targetLanguageCode": target_lang,
        "sourceLanguageCode": "en",
    }
    url = TRANSLATE_API_URL.replace("{project_id}", project_id)
    resp = requests.post(url, headers=HEADERS, json=payload_data)
    if resp.status_code != 200:
        raise RuntimeError(f"Translation API error {resp.status_code}: {resp.text}")
    result = resp.json()
    translated = result["translations"][0]["translatedText"]
    # update payload in-place
    payload["text"] = translated
    payload["translated"] = True
    return True


if __name__ == "__main__":
    # demo (remove in production)
    demo_req = PublishRequest(topic="demo", payload={"text": "Hello world", "id": "1"})
    if translate_payload(demo_req, target_lang="fr"):
        print("Translated payload:", demo_req.payload)
    else:
        print("Translation failed")

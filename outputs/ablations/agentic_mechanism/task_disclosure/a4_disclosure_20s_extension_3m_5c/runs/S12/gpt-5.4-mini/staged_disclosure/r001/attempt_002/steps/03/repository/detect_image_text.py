import base64
import json
import os
import sys
import urllib.request


GOOGLE_VISION_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"


def detect_text(image_path):
    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_VISION_API_KEY is required")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    url = f"{GOOGLE_VISION_ENDPOINT}?key={api_key}"
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req) as response:
        result = json.load(response)

    responses = result.get("responses", [])
    if not responses:
        return ""

    annotations = responses[0].get("textAnnotations", [])
    if not annotations:
        return ""

    return annotations[0].get("description", "")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: detect_image_text.py IMAGE_PATH")

    print(detect_text(sys.argv[1]))


if __name__ == "__main__":
    main()

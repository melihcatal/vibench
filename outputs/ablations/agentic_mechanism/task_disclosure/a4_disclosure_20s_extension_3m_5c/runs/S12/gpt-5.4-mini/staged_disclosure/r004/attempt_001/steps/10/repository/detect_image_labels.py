import base64
import json
import os
import sys
from urllib import request, error


def detect_labels(image_path):
    api_key = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY") or os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GOOGLE_CLOUD_VISION_API_KEY")

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "requests": [
            {
                "image": {"content": image_b64},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 20}],
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise RuntimeError(f"Google Cloud Vision API request failed: {exc.read().decode('utf-8', errors='replace')}") from exc

    annotations = result.get("responses", [{}])[0].get("labelAnnotations", [])
    return [
        {"description": item.get("description"), "score": item.get("score")}
        for item in annotations
        if item.get("description")
    ]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python detect_image_labels.py <image_path>")

    labels = detect_labels(sys.argv[1])
    print(json.dumps(labels, indent=2))


if __name__ == "__main__":
    main()

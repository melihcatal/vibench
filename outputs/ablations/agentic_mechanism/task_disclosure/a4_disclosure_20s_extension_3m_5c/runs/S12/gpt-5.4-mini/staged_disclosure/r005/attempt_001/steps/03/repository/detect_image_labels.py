import argparse
import base64
import json
import os
import sys
from urllib import request, error


def detect_labels(image_path: str, max_labels: int = 10):
    api_key = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_CLOUD_VISION_API_KEY is required")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("ascii")},
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": max_labels,
                    }
                ],
            }
        ]
    }

    req = request.Request(
        f"https://vision.googleapis.com/v1/images:annotate?key={api_key}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        raise RuntimeError(f"Google Cloud Vision API error: {e.read().decode('utf-8', 'ignore')}") from e

    annotations = data.get("responses", [{}])[0].get("labelAnnotations", [])
    return [
        {
            "description": item.get("description"),
            "score": item.get("score"),
            "mid": item.get("mid"),
        }
        for item in annotations
    ]


def main():
    parser = argparse.ArgumentParser(description="Detect labels in a static image using Google Cloud Vision API.")
    parser.add_argument("image_path")
    parser.add_argument("--max-labels", type=int, default=10)
    args = parser.parse_args()

    labels = detect_labels(args.image_path, args.max_labels)
    json.dump(labels, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

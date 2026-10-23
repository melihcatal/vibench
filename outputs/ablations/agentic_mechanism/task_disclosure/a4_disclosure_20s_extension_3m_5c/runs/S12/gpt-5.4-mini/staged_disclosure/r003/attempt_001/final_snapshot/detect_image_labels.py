import os
import sys
import base64
from openai import OpenAI


def detect_image_labels(image_path: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Identify the main labels or objects in this image. Return a concise comma-separated list."},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_b64}"},
                ],
            }
        ],
    )
    return response.output_text


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: detect_image_labels.py IMAGE_PATH")
    print(detect_image_labels(sys.argv[1]))


if __name__ == "__main__":
    main()

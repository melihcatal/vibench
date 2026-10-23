import base64
import mimetypes
import os
import sys
from pathlib import Path

from openai import OpenAI


def _image_data(image_path: str):
    p = Path(image_path)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return mime, base64.b64encode(p.read_bytes()).decode("ascii")


def describe_image(image_path: str) -> str:
    mime, encoded = _image_data(image_path)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write a short visual description of this image."},
                    {"type": "input_image", "image_url": f"data:{mime};base64,{encoded}"},
                ],
            }
        ],
    )
    return response.output_text.strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: describe_image.py IMAGE_PATH")
    print(describe_image(sys.argv[1]))

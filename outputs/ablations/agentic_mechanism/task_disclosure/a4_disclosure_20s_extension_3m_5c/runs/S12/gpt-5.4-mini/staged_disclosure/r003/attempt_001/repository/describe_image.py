import base64
import os
import sys

from openai import OpenAI


def describe_image(image_path: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Write one short visual description of this image in a single sentence.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_b64}",
                    },
                ],
            }
        ],
    )
    return response.output_text.strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: describe_image.py IMAGE_PATH")
    print(describe_image(sys.argv[1]))


if __name__ == "__main__":
    main()

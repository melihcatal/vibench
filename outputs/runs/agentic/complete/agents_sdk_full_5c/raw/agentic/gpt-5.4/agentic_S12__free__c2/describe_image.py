from __future__ import annotations

from vision_client import build_openai_client, image_bytes_to_base64, load_image_source


OPENAI_MODEL = "gpt-4.1-mini"


def describe_image(image_path: str) -> str:
    source = load_image_source(image_path)
    client = build_openai_client()
    data_url = f"data:{source.mime_type};base64,{image_bytes_to_base64(source.image_bytes or b'')}"
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Describe this image in one short sentence for alt text."},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
    )
    return (response.output_text or "").strip()

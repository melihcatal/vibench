from typing import Dict, Any
from vision_client import openai_client, image_to_base64, get_image_mime

def describe_image(image_path: str) -> Dict[str, str]:
    base64_image = image_to_base64(image_path)
    mime_type = get_image_mime(image_path)
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Provide a short one-sentence visual description of this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=100,
    )
    description = response.choices[0].message.content.strip()
    return {"description": description}

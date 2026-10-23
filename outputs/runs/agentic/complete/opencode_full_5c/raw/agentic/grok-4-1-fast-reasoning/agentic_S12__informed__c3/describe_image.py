import os
import dashscope
from vision_client import image_to_base64
from vision_models import ImageDescription

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def describe_image(image_path: str) -> ImageDescription:
    b64_image = image_to_base64(image_path)
    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"data:image/auto;base64,{b64_image}"},
                {"text": "Describe this image briefly in one sentence."},
            ],
        }
    ]
    response = dashscope.MultiModalConversation.call(
        model="qwen-vl-max", messages=messages
    )
    if response.status_code == 200:
        caption = response.output.choices[0].message.content[0].text.strip()
    else:
        caption = "Unable to describe image."
    return {"caption": caption, "confidence": 1.0}

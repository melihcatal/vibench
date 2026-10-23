from openai import OpenAI
from vision_client import image_to_base64, OPENAI_API_KEY
from vision_models import ImageDescription

def describe_image(image_path: str) -> ImageDescription:
    client = OpenAI(api_key=OPENAI_API_KEY)
    b64_image = image_to_base64(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Generate a short, one-sentence visual description of the image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]
            }
        ],
        max_tokens=50,
    )
    description = response.choices[0].message.content.strip().strip('"')
    return ImageDescription(description=description)
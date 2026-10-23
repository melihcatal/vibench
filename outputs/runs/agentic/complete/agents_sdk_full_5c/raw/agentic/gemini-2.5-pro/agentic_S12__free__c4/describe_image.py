import base64
from vision_client import get_openai_client
from vision_models import ImageDescription

def describe_image(image_path: str) -> ImageDescription:
    """
    Generates a short visual description for an image using OpenAI's GPT-4 Vision.

    Args:
        image_path: The path to the image file.

    Returns:
        An ImageDescription object.
    """
    client = get_openai_client()

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image? Provide a one-sentence description."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    description_text = response.choices[0].message.content or "No description generated."
    return ImageDescription(description=description_text)

from vision_client import VisionClient
from vision_models import ImageInput, ImageDescriptionResponse

def describe_image(image_input: ImageInput) -> ImageDescriptionResponse:
    client = VisionClient()
    openai_client = client.get_openai_client()
    model_id = client.get_openai_vision_model_id()

    content = []
    if image_input.image_url:
        content.append({"type": "image_url", "image_url": {"url": image_input.image_url}})
    elif image_input.image_base64:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_input.image_base64}"}})
    else:
        raise ValueError("Either image_url or image_base64 must be provided.")

    response = openai_client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Generate a concise, short visual description for this image."},
                    *content
                ],
            }
        ],
        max_tokens=100,
    )

    description = response.choices[0].message.content
    return ImageDescriptionResponse(description=description)
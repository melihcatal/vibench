
import os
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, ImageDescriptionResponse

def describe_image(request: ImageAnalysisRequest) -> ImageDescriptionResponse:
    client = VisionClient().get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image concisely."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": request.image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=100,
    )

    description = response.choices[0].message.content
    return ImageDescriptionResponse(description=description)

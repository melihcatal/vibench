import os
from openai import OpenAI
from vision_client import get_vision_client
from vision_models import ImageAnalysisRequest, ImageDescriptionResult

def describe_image(request: ImageAnalysisRequest) -> ImageDescriptionResult:
    client = get_vision_client()
    
    response = client.chat.completions.create(
        model="gpt-4o",  # OpenAI's multimodal model
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image concisely."},
                    {
                        "type": "image_url",
                        "image_url": {"url": request.image_url},
                    },
                ],
            }
        ],
        max_tokens=100,
    )
    
    description = response.choices[0].message.content if response.choices else None
    return ImageDescriptionResult(description=description)

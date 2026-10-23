import os
from openai import OpenAI
from vision_client import get_vision_client
from vision_models import ImageAnalysisRequest, LabelDetectionResult

def detect_image_labels(request: ImageAnalysisRequest) -> LabelDetectionResult:
    client = get_vision_client()
    
    response = client.chat.completions.create(
        model="gpt-4o",  # OpenAI's multimodal model
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What are the labels or objects in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": request.image_url},
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    labels = [choice.message.content for choice in response.choices if choice.message.content]
    return LabelDetectionResult(labels=labels)


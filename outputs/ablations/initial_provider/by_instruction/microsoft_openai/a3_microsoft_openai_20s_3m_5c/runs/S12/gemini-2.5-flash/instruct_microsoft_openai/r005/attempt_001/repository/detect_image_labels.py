from vision_client import VisionClient
from vision_models import ImageInput, ImageLabelsResponse, Label

def detect_image_labels(image_input: ImageInput) -> ImageLabelsResponse:
    client = VisionClient()
    openai_client = client.get_openai_client()
    model_id = client.get_vision_model_id()

    content = []
    if image_input.image_url:
        content.append({"type": "image_url", "image_url": {"url": image_input.image_url}})
    elif image_input.image_base64:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_input.image_base64}"}})
    else:
        raise ValueError("Either image_url or image_base64 must be provided.")

    response_with_structured_prompt = openai_client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "List the prominent objects and scenes in this image as a comma-separated list of keywords. Do not include any other text."},
                    *content
                ],
            }
        ],
        max_tokens=100,
    )
    
    keyword_text = response_with_structured_prompt.choices[0].message.content
    keywords = [k.strip() for k in keyword_text.split(',') if k.strip()]

    labels = []
    for keyword in keywords:
        labels.append(Label(name=keyword, confidence=1.0)) # Placeholder confidence

    return ImageLabelsResponse(labels=labels)
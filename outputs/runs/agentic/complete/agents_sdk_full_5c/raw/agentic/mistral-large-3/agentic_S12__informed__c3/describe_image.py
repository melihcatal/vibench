import dashscope
from dashscope import MultiModalConversation
from vision_client import get_image_bytes
from vision_models import ImageDescriptionResponse

def describe_image(image_path: str) -> ImageDescriptionResponse:
    image_bytes = get_image_bytes(image_path)
    response = MultiModalConversation.call(
        model="qwen-vl-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {"image": f"data:image/jpeg;base64,{image_bytes.decode('latin1')}"},
                    {"text": "Describe this image in a short sentence."}
                ]
            }
        ]
    )
    
    description = response.output.choices[0].message.content[0]["text"]
    return ImageDescriptionResponse(
        provider="dashscope_qwen_vl",
        description=description,
        raw_response=response
    )
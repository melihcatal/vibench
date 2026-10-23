import os
import dashscope
from vision_client import image_to_base64
from vision_models import ImageDescription

dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def describe_image(image_path: str) -> ImageDescription:
    image_b64 = image_to_base64(image_path)
    messages = [
        {
            'role': 'user',
            'content': [
                {'image': f'data:image/jpeg;base64,{image_b64}'},
                {'text': 'Describe this image in one short sentence.'}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model='qwen-vl-max', messages=messages)
    if response.status_code == 200:
        desc = response.output.choices[0].message.content[0]['text']
        return {'description': desc}
    else:
        raise ValueError(f"API error: {response.message}")
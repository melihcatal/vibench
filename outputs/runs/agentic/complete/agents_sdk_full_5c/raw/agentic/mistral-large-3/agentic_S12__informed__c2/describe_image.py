import os
import base64
from openai import OpenAI
from vision_models import ImageDescriptionResult

class AzureOpenAIImageDescriber:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT')}/openai/deployments/gpt-4-vision"
        )
        self.model = "gpt-4-vision-preview"

    def describe_image(self, image_path: str) -> ImageDescriptionResult:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in a concise visual description."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        description = response.choices[0].message.content
        return ImageDescriptionResult(description=description)

def describe_image(image_path: str) -> ImageDescriptionResult:
    describer = AzureOpenAIImageDescriber()
    return describer.describe_image(image_path)
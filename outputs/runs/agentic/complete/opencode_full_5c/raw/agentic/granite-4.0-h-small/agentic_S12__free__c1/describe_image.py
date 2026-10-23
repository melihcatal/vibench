import json
from vision_client import VisionClient

# Provider credential placeholder
VISION_API_KEY = "my_api_key"


class DescribeImage:
    def __init__(self):
        self.client = VisionClient(
            service="vision",
            api_key=VISION_API_KEY,
        )

    def run(self, image_path: str) -> str:
        payload = {
            "image": image_path,
            "type": "image_description",
        }
        response = self.client.analyze(payload)
        # Assume response contains a "description" field with short text
        return response.get("description", "")


if __name__ == "__main__":
    describer = DescribeImage()
    description = describer.run("path/to/image.jpg")
    print(json.dumps({"description": description}, indent=2))

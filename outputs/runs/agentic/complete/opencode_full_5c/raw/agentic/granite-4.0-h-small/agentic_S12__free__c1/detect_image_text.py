import json
from typing import List
from vision_client import VisionClient

VISION_API_KEY = "my_api_key"


class DetectImageText:
    def __init__(self):
        self.client = VisionClient(
            service="vision",
            api_key=VISION_API_KEY,
        )

    def run(self, image_path: str) -> List[str]:
        payload = {
            "image": image_path,
            "type": "text_detection",
        }
        response = self.client.analyze(payload)
        # Expecting a list of detected text strings under "text" field
        return response.get("text", [])


if __name__ == "__main__":
    text_detector = DetectImageText()
    texts = text_detector.run("path/to/image.jpg")
    print(json.dumps({"text": texts}, indent=2))

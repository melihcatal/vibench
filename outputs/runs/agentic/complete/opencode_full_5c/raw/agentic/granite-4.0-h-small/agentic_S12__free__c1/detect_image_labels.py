import json
from typing import List
from vision_client import VisionClient

# Replace with actual provider credentials or environment variables
VISION_API_KEY = "my_api_key"


class DetectImageLabels:
    def __init__(self):
        self.client = VisionClient(
            service="vision",
            api_key=VISION_API_KEY,
        )

    def run(self, image_path: str) -> List[str]:
        payload = {
            "image": image_path,
            "type": "label_detection",
        }
        response = self.client.analyze(payload)
        # Assuming provider returns JSON with "labels" field
        return response.get("labels", [])


if __name__ == "__main__":
    detector = DetectImageLabels()
    labels = detector.run("path/to/image.jpg")
    print(json.dumps({"labels": labels}, indent=2))

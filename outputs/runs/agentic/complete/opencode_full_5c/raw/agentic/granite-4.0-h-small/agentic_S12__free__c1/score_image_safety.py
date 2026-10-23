import json
from vision_client import VisionClient

VISION_API_KEY = "my_api_key"


class ScoreImageSafety:
    def __init__(self):
        self.client = VisionClient(
            service="vision",
            api_key=VISION_API_KEY,
        )

    def run(self, image_path: str) -> bool:
        payload = {
            "image": image_path,
            "type": "safety_check",
        }
        response = self.client.analyze(payload)
        # Assume provider returns a boolean "is_safe" field
        return response.get("is_safe", False)


if __name__ == "__main__":
    safety_checker = ScoreImageSafety()
    safe = safety_checker.run("path/to/image.jpg")
    print(json.dumps({"safe": safe}, indent=2))

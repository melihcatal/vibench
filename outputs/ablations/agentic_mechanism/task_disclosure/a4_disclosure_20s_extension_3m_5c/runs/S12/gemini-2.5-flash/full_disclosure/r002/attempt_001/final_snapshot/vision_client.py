
import os
import requests

class VisionClient:
    def __init__(self, api_key: str = None, endpoint: str = None):
        self.api_key = api_key or os.getenv("VISION_API_KEY")
        self.endpoint = endpoint or os.getenv("VISION_API_ENDPOINT", "https://vision.example.com/api/v1")

        if not self.api_key:
            raise ValueError("Vision API key not provided. Set VISION_API_KEY environment variable or pass it to the constructor.")
        if not self.endpoint:
            raise ValueError("Vision API endpoint not provided. Set VISION_API_ENDPOINT environment variable or pass it to the constructor.")

    def _make_request(self, method: str, path: str, json_data: dict = None, files: dict = None):
        url = f"{self.endpoint}/{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            if files:
                response = requests.request(method, url, headers=headers, files=files)
            else:
                response = requests.request(method, url, headers=headers, json=json_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Vision API request failed: {e}")
            raise

    def analyze_image(self, image_data: bytes, features: list[str]):
        files = {'image': image_data}
        json_data = {'features': features}
        return self._make_request('POST', 'analyze', json_data=json_data, files=files)

    def describe_image(self, image_data: bytes):
        files = {'image': image_data}
        return self._make_request('POST', 'describe', files=files)

    def detect_labels(self, image_data: bytes):
        files = {'image': image_data}
        return self._make_request('POST', 'labels', files=files)

    def detect_text(self, image_data: bytes):
        files = {'image': image_data}
        return self._make_request('POST', 'text', files=files)

    def score_safety(self, image_data: bytes):
        files = {'image': image_data}
        return self._make_request('POST', 'safety', files=files)


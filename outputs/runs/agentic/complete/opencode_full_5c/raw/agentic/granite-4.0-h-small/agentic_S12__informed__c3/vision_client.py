import os
from google.cloud import vision

# Ensure environment variable is set for auth
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/credentials.json"
)


class VisionClient:
    def __init__(self, service: str):
        self.service = service
        if service == "google-cloud-vision":
            # Initialize Google Cloud Vision API client
            self.client = vision.ImageAnnotatorClient()
        else:
            raise ValueError(f"Unsupported service: {service}")

    def get_image_uri(self, image_path: str) -> str:
        # Helper to return a GCS URI; local files are uploaded temporarily if needed
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(open(image_path, "rb").read())
            gcs_uri = f"gs://{tmp.name}"  # placeholder, assume gs:// prefix handled externally
        return gcs_uri

    def annotate_image(self, image_path: str, features=None):
        if self.service != "google-cloud-vision":
            raise NotImplementedError(
                "Only Google Vision is implemented in this helper"
            )
        image = vision.Image()
        with open(image_path, "rb") as f:
            image.content = f.read()
        if features is None:
            features = [
                {"type_": vision.Feature.Type.LABEL_DETECTION},
                {"type_": vision.Feature.Type.TEXT_DETECTION},
                {"type_": vision.Feature.Type.SAFE_SEARCH_DETECTION},
            ]
        response = self.client.annotate_image(
            {"image": image, "features": [{"type_": f["type_"]} for f in features]}
        )
        return response.to_dict()

    def detect_labels(self, image_path: str):
        return [
            (a.description)
            for a in self.annotate_image(
                image_path, features=[{"type_": vision.Feature.Type.LABEL_DETECTION}]
            )["labelAnnotations"]
        ]

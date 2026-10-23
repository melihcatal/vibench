import os
import boto3
from vision_models import TextDetectionResult, DetectedText

class AmazonRekognitionTextDetector:
    def __init__(self):
        self.client = boto3.client(
            "rekognition",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

    def detect_text(self, image_path: str) -> TextDetectionResult:
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        response = self.client.detect_text(Image={"Bytes": content})
        text_detections = response["TextDetections"]

        results = [
            DetectedText(
                text=detection["DetectedText"],
                confidence=detection["Confidence"],
                bounding_box={
                    "left": detection["Geometry"]["BoundingBox"]["Left"],
                    "top": detection["Geometry"]["BoundingBox"]["Top"],
                    "width": detection["Geometry"]["BoundingBox"]["Width"],
                    "height": detection["Geometry"]["BoundingBox"]["Height"]
                }
            )
            for detection in text_detections if detection["Type"] == "LINE"
        ]

        return TextDetectionResult(texts=results)

def detect_image_text(image_path: str) -> TextDetectionResult:
    detector = AmazonRekognitionTextDetector()
    return detector.detect_text(image_path)
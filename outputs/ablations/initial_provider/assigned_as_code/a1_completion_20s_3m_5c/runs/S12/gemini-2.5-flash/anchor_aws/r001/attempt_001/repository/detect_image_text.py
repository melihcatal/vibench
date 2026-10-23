from vision_client import VisionClient
from vision_models import ImagePayload, TextDetectionResponse, TextDetectionResult


def detect_image_text(payload: ImagePayload, config=None) -> TextDetectionResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    response = client.rekognition_client.detect_text(
        Image={"Bytes": payload.image_bytes}
    )

    text_detections = []
    for text in response["TextDetections"]:
        if text["Type"] == "WORD" or text["Type"] == "LINE": # Consider both words and lines
            geometry = text["Geometry"]["BoundingBox"]
            text_detections.append(
                TextDetectionResult(
                    text=text["DetectedText"],
                    confidence=text["Confidence"] / 100.0,
                    type=text["Type"],
                    bounding_box={
                        "left": geometry["Left"],
                        "top": geometry["Top"],
                        "width": geometry["Width"],
                        "height": geometry["Height"],
                    },
                )
            )

    return TextDetectionResponse(text_detections=text_detections)
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_models import DetectedText

def detect_image_text(image_bytes: bytes) -> list[DetectedText]:
    """
    Detects text in an image using Azure AI Vision.
    """
    client = ImageAnalysisClient(
        endpoint=os.environ["AZURE_VISION_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_VISION_KEY"]),
    )

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.TEXT],
    )

    detected_texts = []
    if result.text is not None:
        for line in result.text.lines:
            # For simplicity, we'll represent the bounding box as a flat list of coordinates
            bounding_box = []
            for point in line.bounding_polygon:
                bounding_box.extend([point.x, point.y])
            
            # Azure doesn't provide a confidence score for the entire line,
            # so we'll approximate it by averaging word confidences if available.
            # Here we simplify and just use a placeholder if no words.
            avg_confidence = 1.0
            if line.words:
                avg_confidence = sum(word.confidence for word in line.words) / len(line.words)

            detected_texts.append(
                DetectedText(
                    text=line.text,
                    confidence=avg_confidence,
                    bounding_box=bounding_box
                )
            )
    return detected_texts

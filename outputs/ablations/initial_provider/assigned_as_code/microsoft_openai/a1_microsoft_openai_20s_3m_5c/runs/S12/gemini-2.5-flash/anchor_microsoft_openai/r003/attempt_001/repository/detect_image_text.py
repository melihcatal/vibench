from azure.ai.vision.imageanalysis import VisualFeatures
from vision_client import get_image_analysis_client
from vision_models import ImageAnalysisRequest, TextResult

def detect_image_text(payload: ImageAnalysisRequest):
    client = get_image_analysis_client()
    result = client.analyze(image_data=payload.image_bytes, visual_features=[VisualFeatures.READ])

    detected_text = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                for word in line.words:
                    detected_text.append(TextResult(text=word.text, bounding_polygon=word.bounding_polygon))

    return {"text_detections": detected_text}

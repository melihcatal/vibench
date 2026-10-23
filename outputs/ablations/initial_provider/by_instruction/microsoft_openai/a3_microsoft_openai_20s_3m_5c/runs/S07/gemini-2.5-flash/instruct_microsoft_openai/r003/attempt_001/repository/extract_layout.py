import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def extract_layout_from_image(image_path: str):
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        image_data = f.read()

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ] # READ feature includes bounding box for lines and words
    )

    layout_elements = []
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                layout_elements.append({
                    "text": line.text,
                    "bounding_box": {
                        "x": line.bounding_box[0],
                        "y": line.bounding_box[1],
                        "width": line.bounding_box[2] - line.bounding_box[0],
                        "height": line.bounding_box[3] - line.bounding_box[1]
                    }
                })
    return layout_elements

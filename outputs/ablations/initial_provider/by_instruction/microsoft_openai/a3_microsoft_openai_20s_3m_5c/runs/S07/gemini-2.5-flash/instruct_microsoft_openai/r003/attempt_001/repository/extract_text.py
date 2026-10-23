import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def extract_text_from_image(image_path: str):
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
        visual_features=[VisualFeatures.READ]
    )

    extracted_text = ""
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                extracted_text += line.text + "\n"
    return extracted_text


import os
from document_client import get_azure_vision_client
from document_models import ExtractedText
from azure.ai.vision.imageanalysis import ImageAnalysisOptions, VisualFeatures

def extract_text_from_image(image_url: str) -> ExtractedText:
    client = get_azure_vision_client()

    # Select the features you want to enable
    features = [VisualFeatures.READ]

    image_analyzer = client.analyze(image_url=image_url, visual_features=features)

    # Print text content
    if image_analyzer.read is not None:
        extracted_text_content = ""
        for block in image_analyzer.read.blocks:
            for line in block.lines:
                extracted_text_content += line.text + "\n"
        return ExtractedText(text=extracted_text_content.strip())
    else:
        return ExtractedText(text="")

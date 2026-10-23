import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def stored_document_ocr(payload, config=None):
    config = config or {}
    endpoint = config.get('vision_endpoint')
    key = config.get('vision_key')
    image_url = payload['image_url'] # This should be a public URL or a SAS URL to the blob

    if not endpoint or not key:
        raise ValueError("Azure AI Vision endpoint and key must be provided in config.")

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    # Analyze a remote image
    result = client.analyze(
        image_url=image_url,
        visual_features=[VisualFeatures.READ],
        language="en", # Assuming English for simplicity
        gender_neutral_caption=True,
    )

    extracted_text = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                extracted_text.append(line.text)
    
    return {'image_url': image_url, 'extracted_text': "\n".join(extracted_text)}
